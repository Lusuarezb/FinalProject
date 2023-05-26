from pygame import mixer

def select_sounds(theme):
    mixer.music.load(f"media/{theme}/Tetris_theme_{theme.lower()}.mp3")
    sounds = {}
    sounds["clear_row"] = mixer.Sound(f"media/{theme}/Clear_row.mp3")
    sounds["lose"] = mixer.Sound(f"media/{theme}/Lose.mp3")
    sounds["place"] = mixer.Sound(f"media/{theme}/Place.mp3")
    sounds["rotate"] = mixer.Sound(f"media/{theme}/Rotate.mp3")

    set_volumes(theme, sounds)

    return sounds


def set_volumes(theme, sounds):
    if theme == "Normal":
        mixer.music.set_volume(0.1)
        sounds["clear_row"].set_volume(0.3)
        sounds["lose"].set_volume(0.1)
        sounds["place"].set_volume(0.1)
        sounds["rotate"].set_volume(0.5)
    elif theme == "Metal":
        mixer.music.set_volume(1)
        sounds["clear_row"].set_volume(0.3)
        sounds["lose"].set_volume(0.1)
        sounds["place"].set_volume(0.1)
        sounds["rotate"].set_volume(0.5)


def select_colors(theme):
    return


def select_background(theme):
    return