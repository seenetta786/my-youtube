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

client.on('ready', async () => {
    console.log('Client is ready!');
    const chats = await client.getChats();
    console.log('--- GROUP LIST ---');
    chats.forEach(chat => {
        if (chat.isGroup) {
            console.log(`Name: "${chat.name}" | ID: ${chat.id._serialized}`);
        }
    });
    console.log('--- END LIST ---');
    process.exit(0);
});

client.initialize();
