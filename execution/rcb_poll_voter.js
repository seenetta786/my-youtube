const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const fs = require('fs');
const path = require('path');

// Configuration
const TARGET_ID = '919481546119@c.us';
const LOG_DIR = path.join(__dirname, '..', '.tmp');
const LOG_FILE = path.join(LOG_DIR, 'poll_voter.log');

// Ensure log directory exists
if (!fs.existsSync(LOG_DIR)) {
    fs.mkdirSync(LOG_DIR, { recursive: true });
}

const HISTORY_FILE = path.join(LOG_DIR, 'poll_history.json');

// --- Persistence Helpers ---
function loadVotedPolls() {
    try {
        if (fs.existsSync(HISTORY_FILE)) {
            const data = fs.readFileSync(HISTORY_FILE, 'utf8');
            const history = JSON.parse(data);
            return new Set(history.votedPolls || []);
        }
    } catch (err) {
        log(`Error loading history: ${err.message}`);
    }
    return new Set();
}

function saveVotedPolls(set) {
    try {
        const data = JSON.stringify({ votedPolls: Array.from(set) }, null, 2);
        fs.writeFileSync(HISTORY_FILE, data, 'utf8');
    } catch (err) {
        log(`Error saving history: ${err.message}`);
    }
}

// --- Voting Helper ---
async function voteForOption(message, targetOptionText) {
    try {
        const options = message.pollOptions;
        if (!options || !Array.isArray(options)) {
            log(`ERROR: No poll options found for message ${message.id._serialized}`);
            return false;
        }

        // Find option matching target (case-insensitive, trimmed)
        const match = options.find(opt =>
            opt.name.trim().toLowerCase() === targetOptionText.trim().toLowerCase()
        );

        if (match) {
            log(`Found option "${match.name}" matching "${targetOptionText}". Voting...`);
            await message.vote([match.name]);
            log(`Successfully voted for "${match.name}"`);
            return true;
        } else {
            log(`WARNING: Could not find option matching "${targetOptionText}". Available options: ${options.map(o => `"${o.name}"`).join(', ')}`);
            return false;
        }
    } catch (err) {
        log(`ERROR voting for option: ${err.message}`);
        return false;
    }
}

function log(message) {
    const timestamp = new Date().toISOString();
    const logEntry = `${timestamp} - ${message}\n`;
    console.log(logEntry.trim());
    fs.appendFileSync(LOG_FILE, logEntry);
}

process.on('uncaughtException', (err) => {
    log(`UNCAUGHT EXCEPTION: ${err.message}\n${err.stack}`);
});

process.on('unhandledRejection', (reason, promise) => {
    log(`UNHANDLED REJECTION: ${reason}`);
});

// Initialize WhatsApp client with persistent session
const client = new Client({
    authStrategy: new LocalAuth({
        dataPath: path.join(__dirname, '..', '.wwebjs_auth')
    }),
    puppeteer: {
        headless: true,
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-accelerated-2d-canvas',
            '--no-first-run',
            '--no-zygote',
            '--single-process', // Can help in constrained environments
            '--disable-gpu'
        ]
    }
});

// QR Code event - display for first-time authentication
client.on('qr', (qr) => {
    log('QR Code received. Scan with WhatsApp:');
    qrcode.generate(qr, { small: true });
});

// Polling mechanism to ensure we don't miss polls (redundancy for weak events)
const CHECK_INTERVAL = 60000; // Check every 60 seconds
const votedPolls = loadVotedPolls(); // Load from file
log(`Loaded ${votedPolls.size} previously voted polls.`);

async function checkRecentPolls() {
    try {
        const chat = await client.getChatById(TARGET_ID);
        const messages = await chat.fetchMessages({ limit: 10 });

        for (const message of messages) {
            if (message.type === 'poll_creation') {
                const pollId = message.id._serialized;

                // Avoid re-voting in the same session excessively
                // (Though re-voting is harmless, it updates the vote)
                if (votedPolls.has(pollId)) continue;

                // Check timestamp - only vote on polls from the last 24 hours
                const messageTime = message.timestamp * 1000;
                const oneDayAgo = Date.now() - (24 * 60 * 60 * 1000);

                if (messageTime > oneDayAgo) {
                    log(`Polling found poll: "${message.body}"`);
                    log(`DEBUG: Poll options: ${JSON.stringify(message.pollOptions)}`);

                    const success = await voteForOption(message, 'Yes');
                    if (success) {
                        votedPolls.add(pollId);
                        saveVotedPolls(votedPolls); // Save immediately
                        log(`Voted "Yes" on poll found via polling`);
                    }
                }
            }
        }
    } catch (error) {
        log(`Error in polling loop: ${error.message}`);
    }
}

client.on('ready', async () => {
    log('WhatsApp client is ready and connected!');
    // Start polling
    setInterval(checkRecentPolls, CHECK_INTERVAL);
    // Initial check
    setTimeout(checkRecentPolls, 5000);
});

client.on('loading_screen', (percent, message) => {
    log(`Loading: ${percent}% - ${message}`);
});

client.on('change_state', state => {
    log(`State changed to: ${state}`);
});

// Authentication success
client.on('authenticated', () => {
    log('Authentication successful. Session saved.');
});

// Authentication failure
client.on('auth_failure', (msg) => {
    log(`Authentication failed: ${msg}`);
});

// Disconnection event
client.on('disconnected', (reason) => {
    log(`Client disconnected: ${reason}`);
});

// Message event - listen for incoming polls
client.on('message', async (message) => {
    try {
        // Check if message is from target and is a poll
        if (message.from === TARGET_ID && message.type === 'poll_creation') {
            log(`Poll received in RCB group: "${message.body}"`);

            // Vote for "Yes" using robust helper
            await voteForOption(message, 'Yes');
        }
    } catch (error) {
        log(`Error processing message: ${error.message}`);
    }
});

// Handle message_create for polls we send ourselves
client.on('message_create', async (message) => {
    try {
        // Also catch polls in chats we're part of
        if (message.to === TARGET_ID && message.type === 'poll_creation') {
            log(`Poll detected (message_create): "${message.body}"`);
            const success = await voteForOption(message, 'Yes');
            if (success) {
                log(`Voted "Yes" on poll via message_create`);
            }
        }
    } catch (error) {
        log(`Error in message_create: ${error.message}`);
    }
});

log('Starting RCB Poll Voter...');
client.initialize();
