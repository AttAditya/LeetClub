async function refreshUser(username) {
    await fetch(`/api/users/${username}/refresh`);
}

async function refreshData() {
    let spinner = document.getElementById("refresh-spinner");
    let leaderboardList = document.getElementById("leaderboard-list");

    if (spinner) {
        spinner.classList.add("fa-spin");
        spinner.parentElement.disabled = true;
    }

    if (leaderboardList) {
        leaderboardList.innerHTML = "";
    }

    let response = await fetch("/api/users");
    let usersList = await response.json();

    for (let userData of usersList) {
        console.log(`Refreshing: @${userData.username}`);
        await refreshUser(userData.username);
    }

    console.log("Refreshing completed");

    if (spinner) {
        spinner.classList.remove("fa-spin");
        setTimeout(() => {
            spinner.parentElement.disabled = false;
        }, 15000);
    }

    loadLeaderboard();
}

function addRankCard(data) {
    let list = document.getElementById("leaderboard-list");
    let cardTemplate = `
        <a class="leaderboard-card" href="https://leetcode.com/${data.username}">
            <div class="details">
                <div class="data">
                    <div class="image">
                        <img src="${data.userAvatar}" alt="User Avatar">
                    </div>

                    <div class="info">
                        <div class="name">
                            <h1 class="real-name">
                                ${data.realName}
                            </h1>
                            <h2 class="username">
                                ${data.username}
                            </h2>
                        </div>
                    </div>
                </div>

                <div class="stats">
                    <!--div class="global-ranking">
                        <h2>
                            Global Ranking
                        </h2>
                        <h1>
                            ${data.ranking}
                        </h1>
                    </div>

                    <div class="top">
                        <h2>
                            Top
                        </h2>
                        <h1>
                            ${data.topPercentage}%
                        </h1>
                    </div>

                    <div class="contests">
                        <h2>
                            Contests
                        </h2>
                        <h1>
                            ${data.attendedContestsCount}
                        </h1>
                    </div-->

                    <div class="streak">
                        <h2>
                            Streak
                        </h2>
                        <h1>
                            ${data.streak}
                        </h1>
                    </div>

                    <div class="rating">
                        <h2>
                            Rating
                        </h2>
                        <h1>
                            ${Math.floor(data.rating)}
                        </h1>
                    </div>

                    <div class="question-count">
                        <h2>
                            Questions
                        </h2>
                        <h1>
                            ${data.questionCount}
                        </h1>
                    </div>
                </div>
            </div>
        </div>
    `;

    list.innerHTML += cardTemplate;
}

async function loadLeaderboard() {
    let response = await fetch("/api/users");
    let usersList = await response.json();

    for (let userData of usersList) {
        addRankCard(userData);
    }
}

