# -*- coding: utf-8 -*-
# Copyright: Julien Baley <julien.baley@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

# USER MANUAL:
# This add-on lets the user add the no_sound_in_clz modifier to their
# templates so that only the sounds that are being clozed in the current card
# are played.
# Simply edit your template {{cloze:Text}} to {{no_sound_in_clz:cloze:Text}}

## THE CODE THEREAFTER SHOULDN'T BE MODIFIED UNLESS YOU KNOW WHAT YOU DO ##

from anki.hooks import addHook
import re


class Hook():
    def __init__(self, name):
        addHook('fmod_'+name, self.remove_sound_from_cloze)
  
    def remove_sound_from_cloze(self, txt, exc, *_):
        # save all the clozes in a list and scramble them
        cloze_span = '<span class=cloze>(?:(?!</span>).)*</span>'
        clozes = list()
        for i, m in enumerate(re.findall(cloze_span, txt)):
            txt = txt.replace(m, 'CLZ' + str(i))
            clozes.append(m)

        # delete all the sounds that remain
        sound = '\[sound:.*?]'
        txt = re.sub(sound, '', txt)
        
        # restore clozes
        for i, m in enumerate(clozes):
            txt = txt.replace('CLZ' + str(i), m)
        return txt


#ADD YOUR HOOKS HERE
Hook(name='no_sound_in_clz')
