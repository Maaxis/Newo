import org
from org import *
from personality import personality
import ndimtools as ndim
import typing


def main():
    game = Game("Nineveh","void1")
    tribes = create_tribes(game, "Argon", "Krypton", "Radon")
    #for tribe in game.tribes:
    #    print(tribe.name)
    cast = create_players(game, "Carmen", "Desi", "Ibrahim", "Isabela", "Kenji", "Lachlan", "Layla", "Mae", "Miles", "Narcissa", "Niamh", "Noah", "Piper", "Quinn", "Skye", "Slade", "Sung", "Vance")
    #for player in game.players:
    #    print(player.name)
    tribes_dict = {
        "Carmen": "Argon",
        "Desi": "Radon",
        "Ibrahim": "Argon",
        "Isabela": "Krypton",
        "Kenji": "Radon",
        "Lachlan": "Argon",
        "Layla": "Argon",
        "Mae": "Radon",
        "Miles": "Argon",
        "Narcissa": "Argon",
        "Niamh": "Krypton",
        "Noah": "Radon",
        "Piper": "Radon",
        "Quinn": "Krypton",
        "Skye": "Radon",
        "Slade": "Krypton",
        "Sung": "Krypton",
        "Vance": "Krypton"
    }
    set_tribes_given_names(game, **tribes_dict)
    for tribe in game.tribes:
        player_names = [player.name for player in tribe.players]
        print(f"{tribe.name}: {', '.join(player_names)}")




if __name__ == '__main__':
    main()
