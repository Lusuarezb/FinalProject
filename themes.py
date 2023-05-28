from pygame import mixer, font

mixer.init()


def select_sounds(theme):
    mixer.music.load(f"media/{theme}/Tetris_theme_{theme}.mp3")
    sounds = {
        "clear_row": mixer.Sound(f"media/{theme}/Clear_row_{theme}.mp3"),
        "lose": mixer.Sound(f"media/{theme}/Lose_{theme}.mp3"),
        "place": mixer.Sound(f"media/{theme}/Place_{theme}.mp3"),
        "rotate": mixer.Sound(f"media/{theme}/Rotate_{theme}.mp3")
    }

    set_volumes(theme, sounds)

    return sounds


def set_volumes(theme, sounds):
    if theme == "normal":
        mixer.music.set_volume(0.1)
        sounds["clear_row"].set_volume(0.3)
        sounds["lose"].set_volume(0.1)
        sounds["place"].set_volume(0.1)
        sounds["rotate"].set_volume(0.5)
    elif theme == "metal":
        mixer.music.set_volume(1)
        sounds["clear_row"].set_volume(0.2)
        sounds["lose"].set_volume(0.6)
        sounds["place"].set_volume(0.7)
        sounds["rotate"].set_volume(0.5)


def select_colors(theme):
    pass


def select_font(theme, size):
    try:
        return font.Font(f"media/{theme}/Font_{theme}.ttf", size)
    except:
        return font.Font(f"media/{theme}/Font_{theme}.otf", size)