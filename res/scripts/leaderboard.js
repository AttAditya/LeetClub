function addRankCard(data) {
    let list = document.getElementById("leaderboard-list");
    let cardTemplate = `
        <div class="leaderboard-card">
            <div class="image">
                <img src="${data.userAvatar}" alt="User Avatar">
            </div>

            <div class="details">
                <div class="data">
                    <div class="name">
                        <h1 class="real-name">
                            ${data.realName}
                        </h1>
                        <h2 class="username">
                            ${data.username}
                        </h2>
                    </div>
                </div>

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

