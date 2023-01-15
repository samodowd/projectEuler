"A bag contains one red disc and one blue disc. "
"In a game of chance a player takes a disc at random "
"and its colour is noted. After each turn the disc is "
"returned to the bag, an extra red disc is added, and "
"another disc is taken at random."

"The player pays £1 to play and wins if they have taken "
"more blue discs than red discs at the end of the game."

"If the game is played for four turns, the probability "
"of a player winning is exactly 11/120, and so the maximum "
"prize fund the banker should allocate for winning in this "
"game would be £10 before they would expect to incur a loss."
"Note that any payout will be a whole number of pounds "
"and also includes the original £1 paid to play the game,"
"so in the example given the player actually wins £9."

"Find the maximum prize fund that should be allocated "
"to a single game in which fifteen turns are played."

import numpy as np
import math
import itertools as it
List = "List"


def generate_win_loss_permutations(wins: int, losses: int):
    combination = []
    for win in range(0, wins):
        combination.append('w')
    for lose in range (0, losses):
        combination.append('l')
    # all_permutations = list(set(it.permutations(combination)))
    all_permutations = list(place_losses(losses=losses, length = wins + losses))
    print(all_permutations)

    return all_permutations

def place_losses(losses: int, length: int):
    for positions in it.combinations(range(length), losses):
        p = ['w'] * length

        for i in positions:
            p[i] = "l"

        yield p


def calc_prob_of_win_loss_combo(wins_losses: str):
    game = 0
    probabilities = []
    no_games = len(wins_losses)
    win_probabilities = get_prob_of_win_for_games(no_games)
    for result in wins_losses:
        if result == "w":
            probability = win_probabilities[game]
        elif result == "l":
            probability = 1 - win_probabilities[game]
        else:
            print("Result not recognised")
            probability = np.nan
        probabilities.append(probability)
        game = game + 1

    prob_of_game_combo = np.product(probabilities)

    return prob_of_game_combo


def get_prob_of_win_for_games(no_of_games: int):
    win_probabilities = []
    for i in range(1, no_of_games + 1):
        prob_of_win = 1 / (i + 1)
        win_probabilities.append(prob_of_win)

    return win_probabilities

def get_total_prob_of_win_loss_combo(wins: int, losses:int):
    win_loss_permutations = generate_win_loss_permutations(wins=wins, losses=losses)
    all_probabilities = []
    for combo in win_loss_permutations:
        print(f'combo {combo} starting')
        prob = calc_prob_of_win_loss_combo(combo)
        print(f'combo {combo} finished')
        all_probabilities.append(prob)
    total_probability = np.sum(all_probabilities)

    return total_probability

def get_winning_combinations_for_given_number_of_games(no_games: int):
    min_wins = no_games/2
    max_wins = no_games
    number_of_win_types = math.ceil(max_wins - min_wins)
    win_combinations = []
    wins = max_wins
    losses = 0
    for win_num in range(0, number_of_win_types):
        win_combo = {'wins': wins, 'losses': losses}
        win_combinations.append(win_combo)
        wins -= 1
        losses += 1
    return win_combinations

def get_total_probability_of_winning(no_games: int):
    winning_combos = get_winning_combinations_for_given_number_of_games(no_games=no_games)
    print('combos collected')
    probabilities = []
    for combo in winning_combos:
        print(f'combo {combo} starting')
        probability = get_total_prob_of_win_loss_combo(wins=combo['wins'],
                                         losses=combo['losses'])
        print(f"combo probability = {probability}")
        probabilities.append(probability)

    total_prob = np.sum(probabilities)

    return total_prob

def get_max_prize_fund(no_games):
    probability_of_win = get_total_probability_of_winning(no_games=no_games)
    expected_payoff = 1 / probability_of_win
    max_prize = math.floor(expected_payoff)
    min_dealer_prize = max_prize - 1

    return min_dealer_prize

if __name__ == '__main__':
    print(f"The min prize a dealer should pay is {get_max_prize_fund(15)}")
