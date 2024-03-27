from __future__ import annotations
from typing import Callable
from requests import get

def graphql(
        query: str,
        replace_format: Callable = lambda k: f"[[{k}]]",
        **replace: dict[str, str]|str
    ) -> dict:
    """
    Make a GraphQL request to the LeetCode API.

    :param query: The query to send to the API.
    :param replace_format: The format of the placeholders.
    :param replace: The values to replace the placeholders with.

    :return: The JSON response from the API.
    """

    url: str = "https://leetcode.com/graphql"
    headers: dict = {
        "Content-Type": "application/json"
    }

    for key, value in replace.items():
        query = query.replace(replace_format(key), value) # type: ignore

    response: object = get(url, headers=headers, json={"query": query})

    return response.json()

def contests(username: str) -> dict:
    """
    Get the contest statistics of a user.

    :param username: The username of the user.

    :return: The contest statistics of the user.
    """

    query: str = """
        {
            userContestRanking(username: "[[username]]") {
                attendedContestsCount
                rating
                globalRanking
                totalParticipants
                topPercentage
            }
        }
    """

    return graphql(query, username=username)

def ranking(username: str) -> dict:
    """
    Get the ranking of a user.

    :param username: The username of the user.

    :return: The ranking of the user.
    """

    query: str = """
        {
            matchedUser(username: "[[username]]") {
                profile {
                    ranking
                    userAvatar
                    realName
                }
            }
        }
    """

    return graphql(query, username=username)

def questions(username: str) -> dict:
    """
    Get the question statistics of a user.

    :param username: The username of the user.

    :return: The question statistics of the user.
    """

    query: str = """
        {
            allQuestionsCount {
                difficulty
                count
            }
            matchedUser(username: "[[username]]") {
                problemsSolvedBeatsStats {
                    difficulty
                    percentage
                }
                submitStatsGlobal {
                    acSubmissionNum {
                        difficulty
                        count
                    }
                }
            }
        }
    """

    return graphql(query, username=username)

def data(username: str) -> dict:
    user_data = {
        "username": username,
        "rating": 0,
        "questionCount": 0,
        "streak": 0
    }

    contests_data = contests(username)["data"]
    ranking_data = ranking(username)["data"]
    questions_data = questions(username)["data"]

    contests_data = contests_data["userContestRanking"]
    ranking_data = ranking_data["matchedUser"]["profile"]
    questions_data = questions_data["matchedUser"]["submitStatsGlobal"]
    
    questions_data = questions_data["acSubmissionNum"][0]["count"]


    try:
        user_data.update(ranking_data)
    except:
        pass

    try:
        user_data.update(contests_data)
    except:
        pass

    try:
        user_data.update({"questionCount": questions_data})
    except:
        pass

    return user_data

