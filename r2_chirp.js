const noble = require('@abandonware/noble');

// --- CONFIGURATION ---
// The "Anti-DOS" Service & Characteristic (for the handshake)
const AUTH_SERVICE_UUID = '00020001-574f-4f20-5370-6865726f2121';
const AUTH_CHAR_UUID    = '00020005-574f-4f20-5370-6865726f2121';

// The Main Control Service & Characteristic (for sending commands)
const MAIN_SERVICE_UUID = '00010001-574f-4f20-5370-6865726f2121';
const MAIN_CHAR_UUID    = '00010002-574f-4f20-5370-6865726f2121';

// The Magic Phrase
const MAGIC_PHRASE = "usetheforce...band";

// --- PACKET BUILDER ---
// Constructs a Sphero V2 API packet
function buildPacket(did, cid, data = [], seq = 0x00) {
    // SOP (Start Packet) 0x8D
    // Flags 0x0A (Request Response | Reset Inactivity Timeout)
    // Target 0x01
    const SOP = 0x8D;
    const EOP = 0xD8;
    const TARGET = 0x01;
    
    // Payload for checksum calculation: [DID, CID, SEQ, TARGET, DATA...]
    let payload = [did, cid, seq, TARGET, ...data];
    
    // Checksum: (~sum(payload)) & 0xFF
    let sum = payload.reduce((a, b) => a + b, 0);
    let checksum = (~sum) & 0xFF;
    
    // Construct final buffer
    return Buffer.from([SOP, 0x0A, ...payload, checksum, EOP]);
}

// --- MAIN LOGIC ---

noble.on('stateChange', async (state) => {
    if (state === 'poweredOn') {
        console.log('🤖 Scanning for R2-D2...');
        noble.startScanning([AUTH_SERVICE_UUID], false);
    } else {
        noble.stopScanning();
    }
});

noble.on('discover', async (peripheral) => {
    console.log(`✅ Found: ${peripheral.advertisement.localName || 'Unknown Droid'} (${peripheral.id})`);
    noble.stopScanning();

    peripheral.connect((err) => {
        if (err) return console.error('Connection error:', err);
        console.log('🔌 Connected!');

        // 1. DISCOVER SERVICES
        peripheral.discoverServices([AUTH_SERVICE_UUID, MAIN_SERVICE_UUID], (err, services) => {
            if (err) return console.error(err);

            const authService = services.find(s => s.uuid.replace(/-/g, '') === AUTH_SERVICE_UUID.replace(/-/g, ''));
            const mainService = services.find(s => s.uuid.replace(/-/g, '') === MAIN_SERVICE_UUID.replace(/-/g, ''));

            if (!authService || !mainService) {
                console.error("❌ Could not find required services. Is this R2-D2?");
                process.exit(0);
            }

            // 2. HANDSHAKE (Anti-DOS)
            authService.discoverCharacteristics([AUTH_CHAR_UUID], (err, chars) => {
                const authChar = chars[0];
                console.log('🔐 Sending "usetheforce...band"...');
                
                authChar.write(Buffer.from(MAGIC_PHRASE, 'utf-8'), true, (err) => {
                    if (err) return console.error("Auth failed:", err);
                    console.log('🔓 Unlocked!');

                    // 3. WAKE UP & CHIRP
                    mainService.discoverCharacteristics([MAIN_CHAR_UUID], (err, chars) => {
                        const mainChar = chars[0];

                        // Command 1: WAKE UP
                        // DID: 0x13 (Power), CID: 0x01 (Wake)
                        const wakePacket = buildPacket(0x13, 0x01, [], 0x01);
                        
                        console.log('☀️  Sending Wake Command...');
                        mainChar.write(wakePacket, true, (err) => {
                            
                            // Wait a moment for boot-up
                            setTimeout(() => {
                                // Command 2: PLAY SOUND
                                // DID: 0x1A (IO), CID: 0x18 (Audio)
                                // Data: [0x01 (Play), 0x07 (Sound ID - Happy), 0x00 (Param)]
                                const soundPacket = buildPacket(0x1A, 0x18, [0x01, 0x07, 0x00], 0x02);
                                
                                console.log('🔊 Sending Chirp Command...');
                                mainChar.write(soundPacket, true, (err) => {
                                    if(!err) console.log("🎉 R2-D2 should be chirping!");
                                    
                                    // Disconnect after 3 seconds
                                    setTimeout(() => {
                                        console.log('👋 Disconnecting...');
                                        peripheral.disconnect();
                                        process.exit(0);
                                    }, 3000);
                                });
                            }, 1000); // 1 second delay
                        });
                    });
                });
            });
        });
    });
});