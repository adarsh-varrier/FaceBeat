document.addEventListener('DOMContentLoaded', function () {
    const musicPlayers = document.querySelectorAll('.music-player');

    // Function to pause all other tracks except the currently playing one
    function pauseAllOtherTracks(currentTrack) {
        const allTracks = document.querySelectorAll('audio.music-track');
        allTracks.forEach(track => {
            if (track !== currentTrack && !track.paused) {
                track.pause();
                track.currentTime = 0; // Optionally reset the track to the start
            }
        });
    }

    // Iterate through each music player
    musicPlayers.forEach((player, playerIndex) => {
        const audioTrack = player.querySelector('audio.music-track');
        const prevButton = player.querySelector('.prevButton');
        const nextButton = player.querySelector('.nextButton');

        // When a track starts playing, pause all other tracks
        audioTrack.addEventListener('play', function () {
            pauseAllOtherTracks(audioTrack);
        });

        // When a track ends, automatically play the next one within the same player
        audioTrack.addEventListener('ended', function () {
            const nextPlayer = musicPlayers[playerIndex + 1];
            if (nextPlayer) {
                const nextTrack = nextPlayer.querySelector('audio.music-track');
                if (nextTrack) {
                    nextTrack.play();
                }
            }
        });

        // Event listener for the "Next" button
        nextButton.addEventListener('click', function () {
            const nextPlayer = musicPlayers[playerIndex + 1];
            if (nextPlayer) {
                const nextTrack = nextPlayer.querySelector('audio.music-track');
                if (nextTrack) {
                    nextTrack.play();
                }
            }
        });

        // Event listener for the "Previous" button
        prevButton.addEventListener('click', function () {
            const prevPlayer = musicPlayers[playerIndex - 1];
            if (prevPlayer) {
                const prevTrack = prevPlayer.querySelector('audio.music-track');
                if (prevTrack) {
                    prevTrack.play();
                }
            }
        });
    });
});