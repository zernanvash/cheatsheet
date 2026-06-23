# Fatmike's Crackme #10 (crackmes.one CTF 2026) Writeup

Challenge_URL: https://crackmes.one/crackme/69a2c7347b3cc38c80464d8f

Fatmike's Crackme #10 (crackmes.one CTF 2026)
https://crackmes.one/crackme/69a2c7347b3cc38c80464d8f
To find the function of interest, check the import table for audio-related functions:

waveOutOpen
waveOutPrepareHeader
waveOutWrite

Following the cross-references leads to sub_7FF77B2420F0 — the function responsible for audio output. Tracing back to where it's called from brings us to sub_7FF77B243860.
Just above the call to the audio function there is a jnz branch — this controls whether the music plays or not.
In the same block, before the call to sub_7FF77B2420F0, there are two more functions: sub_7FF77B243A00 and sub_7FF77B243A20. These are responsible for audio distortion.
The distortion functions are controlled by register dl, which is set to 1. Patching mov dl, 1 at addresses 00007FF77B24392D and 00007FF77B243938 to mov dl, 0 solves the crackme.

Flag: CMO{y0u_g0t_r1ckr0ll3d}