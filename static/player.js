// music.kiilolee.com

// Define the tracks that have to be played
let track_list = [
    // {
    // 	audio: "Ali BIrra",
    // 	title: "Nin deema...",
    // 	sid: "music/alibirra_xx_yy_zz.mp3"
    // },
];


let track_name = document.querySelector(".track-name");
let playpause_btn = document.querySelector(".playpause-track");
let next_btn = document.querySelector(".next-track");
let prev_btn = document.querySelector(".prev-track");
let seek_slider = document.querySelector(".seek_slider");
let volume_slider = document.querySelector(".volume_slider");
let curr_time = document.querySelector(".current-time");
let total_duration = document.querySelector(".total-duration");

let track_index = 0;
let isPlaying = false;
let updateTimer;

let curr_track = document.createElement('audio');

let all_songs = document.getElementsByName("music");

for (var i = 0; i < all_songs.length; i++) {
    track_list.push({
        audio: all_songs[i].dataset.audio,
        title: all_songs[i].dataset.title,
        sid: all_songs[i].dataset.sid
    });
}

function loadTrack(track_index) {
    clearInterval(updateTimer);
    resetValues();
    curr_track.src = track_list[track_index].audio;
    curr_track.load();
    track_name.textContent = track_list[track_index].title
    updateTimer = setInterval(seekUpdate, 1000);
    curr_track.addEventListener("ended", nextTrack);
}

function resetValues() {
    curr_time.textContent = "00:00";
    total_duration.textContent = "00:00";
    seek_slider.value = 0;
}

function playpauseTrack() {
    let currsong = document.getElementById(track_list[track_index].sid);
    if (!isPlaying) {
        playTrack();
        if (currsong.classList.contains('fa-3x')) {
            currsong.classList = "fa fa-pause-circle fa-3x";
        }
        else if (currsong.classList.contains('fa-4x')) {
            currsong.classList = "fa fa-pause-circle fa-4x";
        }
        else {
            currsong.classList = "fa fa-pause";
        }
    }
    else {
        pauseTrack();
        if (currsong.classList.contains('fa-3x')) {
            currsong.classList = "fa fa-play-circle fa-3x";
        }
        else if (currsong.classList.contains('fa-4x')) {
            currsong.classList = "fa fa-play-circle fa-4x";
        }
        else {
            currsong.classList = "fa fa-play";
        }
        // currsong.classList = "fa fa-play-circle fa-3x";
    }
}

function playpauseTrack2() {
    if (!isPlaying) {
        curr_track.play();
        isPlaying = true;
        playpause_btn.innerHTML = '<i class="fa fa-pause-circle fa-4x"></i>';
    }
    else {
        curr_track.pause();
        isPlaying = false;
        playpause_btn.innerHTML = '<i class="fa fa-play-circle fa-4x"></i>';
    }
}

function playTrack() {
    curr_track.play();
    isPlaying = true;
    playpause_btn.innerHTML = '<i class="fa fa-pause-circle fa-4x"></i>';
    // change all icons to fa-play
    for (var i = 0; i < track_list.length; i++) {
        let currsong = document.getElementById(track_list[i].sid);
        if (currsong.classList.contains('fa-3x')) {
            currsong.classList = "fa fa-play-circle fa-3x";
        }
        else if (currsong.classList.contains('fa-4x')) {
            currsong.classList = "fa fa-play-circle fa-4x";
        }
        else {
            currsong.classList = "fa fa-play";
        }
    }

    let currsong = document.getElementById(track_list[track_index].sid);
    if (currsong.classList.contains('fa-3x')) {
        currsong.classList = "fa fa-pause-circle fa-3x";
    }
    else if (currsong.classList.contains('fa-4x')) {
        currsong.classList = "fa fa-pause-circle fa-4x";
    }
    else {
        currsong.classList = "fa fa-pause";
    }
}

function playTrack2() {
    curr_track.play();
    isPlaying = true;
    playpause_btn.innerHTML = '<i class="fa fa-pause-circle fa-4x"></i>';
}

function setIndex(n) {
    if (track_index == n) {
        playpauseTrack();
    }
    else {
        track_index = n;
        loadTrack(track_index);
        playTrack();
    }
}

function pauseTrack() {
    curr_track.pause();
    isPlaying = false;
    playpause_btn.innerHTML = '<i class="fa fa-play-circle fa-4x"></i>';
}

function nextTrack() {
    if (track_list.length == 1) {
        playTrack2();
    }
    else {
        if (track_index < track_list.length - 1)
            track_index += 1;
        else track_index = 0;
        loadTrack(track_index);
        playTrack();
    }

}

function prevTrack() {
    if (track_list.length == 1) {
        playTrack2();
    }
    else {
        if (track_index > 0)
            track_index -= 1;
        else track_index = track_list.length - 1;
        loadTrack(track_index);
        playTrack();
    }
}

function seekTo() {
    let seekto = curr_track.duration * (seek_slider.value / 100);
    curr_track.currentTime = seekto;
}

function setVolume() {
    curr_track.volume = volume_slider.value / 100;
}

function seekUpdate() {
    let seekPosition = 0;

    if (!isNaN(curr_track.duration)) {
        seekPosition = curr_track.currentTime * (100 / curr_track.duration);

        seek_slider.value = seekPosition;

        let currentMinutes = Math.floor(curr_track.currentTime / 60);
        let currentSeconds = Math.floor(curr_track.currentTime - currentMinutes * 60);
        let durationMinutes = Math.floor(curr_track.duration / 60);
        let durationSeconds = Math.floor(curr_track.duration - durationMinutes * 60);

        if (currentSeconds < 10) { currentSeconds = "0" + currentSeconds; }
        if (durationSeconds < 10) { durationSeconds = "0" + durationSeconds; }
        if (currentMinutes < 10) { currentMinutes = "0" + currentMinutes; }
        if (durationMinutes < 10) { durationMinutes = "0" + durationMinutes; }

        curr_time.textContent = currentMinutes + ":" + currentSeconds;
        total_duration.textContent = durationMinutes + ":" + durationSeconds;
    }
}


//Run !
if (volume_slider != null) {
    curr_track.volume = volume_slider.value / 100;
    loadTrack(track_index);
}

// Programmer -> @fuadfmb everywhere !