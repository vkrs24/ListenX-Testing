async function searchSong() {
  const query = document.getElementById("searchInput").value;
  const response = await fetch(`http://localhost:8000/search?q=${query}`);
  const data = await response.json();
  console.log(query);

  let resultsDiv = document.getElementById("results");
  resultsDiv.innerHTML = ""; // Clear previous results

  data.forEach((song) => {
    let songDiv = document.createElement("div");
    songDiv.classList.add("song");
    songDiv.innerHTML = `
            <img src="${song.thumbnail}" alt="Thumbnail">
            <div>
                <h3>${song.title}</h3>
                <p>${song.artist}</p>
            </div>
            <button onclick="playAudio('${song.videoId}')">▶ Play</button>
        `;
    resultsDiv.appendChild(songDiv);
  });
}

async function playAudio(videoId) {
  const response = await fetch(
    `http://localhost:8000/get_audio?video_id=${videoId}`
  );
  const data = await response.json();

  if (data.audio_url) {
    let audioPlayer = document.getElementById("audioPlayer");
    audioPlayer.src = data.audio_url;
    audioPlayer.hidden = false;
    audioPlayer.play();
  } else {
    alert("Audio not found!");
  }
}
