"""This module contains the languages for the Translations app."""
from django.utils.translation import get_language
from django.conf import settings


__docformat__ = 'restructuredtext'


_supported_code = {}

_all_codes = None
_all_choices = None

_translation_codes = {}
_translation_choices = {}


def _get_supported_language(lang):
    """Return the `supported language` code of a custom language code."""
    if lang not in _supported_code:
        code = lang.split('-')[0]

        lang_exists = False
        code_exists = False

        # break when the lang is found but not when the code is found
        # cause the code might come before lang and we may miss an accent
        for choice in settings.LANGUAGES:
            if lang == choice[0]:
                lang_exists = True
                break
            if code == choice[0]:
                code_exists = True

        if lang_exists:
            _supported_code[lang] = lang
        elif code_exists:
            _supported_code[lang] = code
        else:
            raise ValueError(
                '`{}` is not a supported language.'.format(lang)
            )
    return _supported_code[lang]


def _get_default_language():
    """Return the `supported language` code of the `default language` code."""
    return _get_supported_language(settings.LANGUAGE_CODE)


def _get_active_language():
    """Return the `supported language` code of the `active language` code."""
    return _get_supported_language(get_language())


def _get_all_languages():
    """Return all the `supported language` codes."""
    global _all_codes
    if _all_codes is None:
        _all_codes = [choice[0] for choice in settings.LANGUAGES]
    return _all_codes


def _get_all_choices():
    """Return all the `supported language` choices."""
    global _all_choices
    if _all_choices is None:
        _all_choices = [
            (None, '---------'),
        ] + [choice for choice in settings.LANGUAGES]
    return _all_choices


def _get_translation_languages():
    """Return the `translation language` codes."""
    default = _get_default_language()
    if default not in _translation_codes:
        _translation_codes[default] = [
            lang for lang in _get_all_languages() if lang != default]
    return _translation_codes[default]


def _get_translation_choices():
    """Return the `translation language` choices."""
    default = _get_default_language()
    if default not in _translation_choices:
        _translation_choices[default] = [
            choice for choice in _get_all_choices() if choice[0] != default]
    return _translation_choices[default]


def _get_translate_language(lang=None):
    """Return the `supported language` code of a preferred language code."""
    if lang is None:
        lang =  _get_active_language()
    else:
        lang = _get_supported_language(lang)

    default = _get_default_language()

    return (lang, lang == default)


def _get_probe_language(lang=None):
    """Return the `supported language` code of a preferred language code."""
    default = _get_default_language()
    if isinstance(lang, (list, tuple)):
        trans_langs = []
        includes_default = False
        for l in lang:
            l = _get_supported_language(l)
            if l == default:
                includes_default = True
            else:
                trans_langs.append(l)
        return (trans_langs, includes_default, True)
    else:
        lang, is_default = _get_translate_language(lang)
        return (lang, is_default, False)


class _LANGUAGE:

    @property
    def DEFAULT(self):
        return _get_default_language()

    @property
    def ACTIVE(self):
        return _get_active_language()

    @property
    def LOOSE(self):
        return [_get_default_language(), _get_active_language()]

    @property
    def ALL(self):
        return _get_all_languages()

languages = _LANGUAGE
