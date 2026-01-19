# Trakt.tv Integration Setup Guide

## Overview
This addon includes **full Trakt.tv integration** for Movies/VOD and Series content. Trakt allows you to:
- Automatically scrobble (track) what you watch
- Sync your watched history across devices
- Add content to your watchlist
- View your viewing statistics

**No API keys needed!** The addon comes with built-in credentials - just sign in and start tracking.

## Setup Instructions

### Step 1: Enable Trakt

1. Open the addon settings in Kodi
2. Navigate to the **Trakt.tv** category
3. Enable **Enable Trakt.tv** toggle
4. Configure additional options:
   - **Auto-Scrobble Playback**: Automatically track what you watch (recommended)
   - **Sync Watchlist**: Sync your Trakt watchlist
   - **Sync Watched Status**: Mark items as watched on Trakt

### Step 2: Sign In to Your Trakt Account

1. From the addon's main menu, select **Trakt.tv**
2. Select **Sign In to Trakt**
3. A dialog will appear showing:
   - URL: `https://trakt.tv/activate`
   - A unique code (example: `ABC-DEF-GH`)
4. On your computer, phone, or tablet:
   - Open a web browser
   - Go to **https://trakt.tv/activate**
   - Log in to your Trakt account (or create one if you don't have it)
   - Enter the code shown on your TV screen
   - Click "Continue" and authorize the app
5. Return to Kodi and click **OK**
6. The addon will check for authorization and confirm success

**That's it!** Your account is now linked.

## Features

### Automatic Scrobbling
When enabled, the addon will automatically:
- Track when you start watching content
- Update progress as you watch
- Mark content as watched when you finish (>90% completion)

### Trakt Menu Options
Access the Trakt menu from the main menu to:
- **Authorize Trakt**: Link your Trakt account
- **Revoke Authorization**: Unlink your account
- **View User Stats**: See your watching statistics
- **Open Trakt Settings**: Quick access to settings

### Supported Content
- **Movies/VOD**: Full scrobbling and sync support
- **TV Series**: Episode tracking with season/episode info

## Troubleshooting

### Sign In Issues
- **"Failed to get device code"**: Check your internet connection and try again
- **"Authorization timeout"**: Make sure you entered the code at trakt.tv/activate within 10 minutes
- **Code expired**: The code expires after 10 minutes - just sign in again to get a new code

### Scrobbling Not Working
- Verify "Auto-Scrobble Playback" is enabled in settings
- Check that "Enable Trakt.tv" is turned on
- Make sure you've signed in to your Trakt account
- Check Kodi logs for Trakt-related errors

### Account Issues
- If you need to switch accounts, use "Sign Out" then sign in again
- Your Trakt credentials are stored securely by Kodi

## Privacy & Security
- Your Trakt credentials are stored locally in Kodi
- OAuth tokens are encrypted by Kodi
- No passwords are transmitted or stored
- Only viewing data is sent to Trakt when scrobbling is enabled

## Advanced Usage

### Manual Tracking
You can manually add items to your Trakt watchlist or mark as watched through the Trakt API when needed.

### Testing
To verify Trakt is working:
1. Watch a movie for at least 1 minute
2. Go to trakt.tv and check your history
3. The movie should appear in your watching history

## Support
For issues specific to Trakt integration:
1. Check Kodi logs for error messages
2. Verify your Trakt account at trakt.tv
3. Test with the official Trakt addon to ensure your account works

## Credits
Trakt.tv API v2
OAuth 2.0 Device Flow Authentication
