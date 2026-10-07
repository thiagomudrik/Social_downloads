# Troubleshooting Guide
## SOCIAL - Developed by Thiago

This guide provides solutions to common issues you may encounter while using SOCIAL.

### 1. TikTok Download Issues

TikTok has the most restrictions. This is the most common source of errors.

**A. "Login Required" or "Video Unavailable"**
- **Cause:** TikTok requires authentication for some private or age-restricted videos. Their anti-bot system also blocks data center IPs.
- **Solution:** 
    1. Test with a public, popular video first.
    2. Update yt-dlp: `pip install -U yt-dlp`
    3. If it persists, the video may be region-locked or private.

**B. Short URL Fails (vm.tiktok.com / vt.tiktok.com)**
- **Cause:** These links need to be resolved to the full URL. On slow or restricted networks, redirection fails.
- **Solution:** Open the short link in your browser first, copy the full `www.tiktok.com/.../video/...` link, and paste that into SOCIAL.

**C. Rate Limiting / HTTP Error 429**
- **Cause:** Downloading too many TikTok videos at once triggers TikTok's rate limit.
- **Solution:** Wait 5-10 minutes and try again. Avoid using batch mode for more than 5 TikTok videos at a time.

**D. Watermarked Videos**
- **Cause:** TikTok serves watermarked versions by default. This is a server-side limitation.
- **Solution:** This is expected behavior. SOCIAL downloads the best available format provided by yt-dlp.

**E. curl_cffi Build Error on Python 3.14 (armv7l)**
- **Cause:** `curl_cffi` requires Rust/Cython to build and fails on older Termux armv7l devices.
- **Solution:** SOCIAL has a built-in fallback. If installation fails, the tool will continue without impersonation. To suppress the error, install without it: `pip install yt-dlp pyfiglet`

### 2. General Download Failures

**"Unsupported URL"**
- Ensure the link is from Facebook, Instagram, TikTok, YouTube, or X. The tool validates URLs before downloading.

**"FFmpeg not found"**
- **Fix:** `pkg install ffmpeg -y` on Termux. FFmpeg is required for merging video and audio.

**No Storage Permission**
- **Fix:** Run `termux-setup-storage` and grant permission. SOCIAL saves to `~/storage/downloads/`.

### 3. Quick Fixes

```bash
# Update the downloader engine
pip install -U yt-dlp

# Reinstall requirements
pip install -r requirements.txt --force-reinstall

# Check ffmpeg
ffmpeg -version
