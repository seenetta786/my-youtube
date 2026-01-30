const { Client, LocalAuth } = require('whatsapp-web.js');
const path = require('path');

const client = new Client({
    authStrategy: new LocalAuth({
        dataPath: path.join(__dirname, '..', '.wwebjs_auth')
    }),
    puppeteer: {
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    }
});

const TARGET_NAME = 'ShYlpa';

client.on('qr', (qr) => {
    console.log('QR Code received!');
    const qrcode = require('qrcode-terminal');
    qrcode.generate(qr, { small: true });
});

client.on('authenticated', () => {
    console.log('Authenticated successfully!');
});

client.on('auth_failure', (msg) => {
    console.log(`Authentication failed: ${msg}`);
});

client.on('ready', async () => {
    console.log('Client is ready!');
    console.log(`Searching for chat: "${TARGET_NAME}"...`);

    try {
        const chats = await client.getChats();
        const matches = chats.filter(c =>
            c.name.toLowerCase().includes(TARGET_NAME.toLowerCase())
        );

        if (matches.length > 0) {
            console.log('--- MATCHES FOUND ---');
            matches.forEach(c => {
                console.log(`Name: ${c.name} | ID: ${c.id._serialized} | isGroup: ${c.isGroup}`);
            });
            console.log('--- END OF MATCHES ---');
        } else {
            console.log('No matches found in active chats.');
        }
    } catch (err) {
        console.error('Error fetching chats:', err);
    }

    process.exit(0);
});

client.initialize();
