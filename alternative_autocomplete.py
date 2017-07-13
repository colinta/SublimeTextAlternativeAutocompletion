import sublime
import sublime_plugin
import re
import os.path


def uniq(list):
    seen = set()
    return [value for value in list if value not in seen and not seen.add(value)]


def fuzzy_match(prefix, word):
    query_i, word_i, next_i = 0, -1, -1
    while query_i < len(prefix):
        word_i = word.find(prefix[query_i], word_i + 1)
        if word_i <= next_i:
            return False
        query_i += 1
        next_i = word_i
    return True


class Candidate:
    def __init__(self, distance, text):
        self.distance = distance
        self.text = text

    def __hash__(self):
        return hash(self.text)

    def __cmp__(self, other):
        return cmp(self.text, other.text)

    def __str__(self):
        return self.text

    def __repr__(self):
        return 'Candidate(text={self.text!r}, distance={self.distance!r})'.format(self=self)


class AlternativeAutocompleteCommand(sublime_plugin.TextCommand):

    candidates = []
    previous_completion = None

    def run(self, edit, cycle='next', tab=False):
        text = self.view.substr(sublime.Region(0, self.view.size()))
        sel = self.view.sel()[0]
        position = sel.b
        prefix_match = re.search(r'([\w\d_]+)\Z', text[:position], re.M | re.U)
        postfix_match = re.search(r'\A([\w\d_]+)', text[position:], re.M | re.U)

        if prefix_match:
            current_prefix = prefix_match.group(1)
            current_search = current_prefix
            replace_start = prefix_match.start(1)
            replace_end = prefix_match.end(1)

            if postfix_match and current_prefix != self.previous_completion:
                replace_end += postfix_match.end(1)
                current_search += postfix_match.group(1)

            if self.previous_completion is None or (current_search != self.previous_completion and current_prefix != self.previous_completion):
                self.previous_completion = None
                self.candidates = self.find_candidates(current_search, position, text)
                if not self.candidates:
                    self.candidates = self.find_candidates(current_prefix, position, text)
                    replace_end = prefix_match.end(1)

                if current_search in self.candidates:
                    self.candidates.remove(current_search)

            self.view.sel().subtract(sel)
            if self.candidates:
                if self.previous_completion is None:
                    completion = self.candidates[0]
                else:
                    if cycle == 'previous':
                        direction = -1
                    else:
                        direction = 1
                    completion = self.candidates[(self.candidates.index(self.previous_completion) + direction) % len(self.candidates)]
                self.view.replace(edit, sublime.Region(replace_start, replace_end), completion)
                self.previous_completion = completion
            else:
                completion = current_search
            cursor = replace_start + len(completion)
            self.view.sel().add(sublime.Region(cursor, cursor))
        elif tab:
            if cycle == 'next':
                if self.view.substr(position) == "\n":
                    self.view.insert(edit, position, "\t")
                else:
                    self.view.run_command('indent')
            else:
                self.view.run_command('unindent')

    @staticmethod
    def get_distance(candidate):
        return candidate.distance

    def find_candidates(self, prefix, position, text):
        default_candidates = self.populate_candidates(prefix)
        candidates = []

        if default_candidates:
            default_candidates.sort(key=self.get_distance)
            if len(default_candidates) > 100:
                default_candidates = default_candidates[0:99]

        word_regex = re.compile(r'\b' + re.escape(prefix[0:1]) + r'[\w\d]+', re.M | re.U | re.I)
        for match in word_regex.finditer(text):
            if match.start() < position < match.end():
                continue
            elif match.end() < position:
                location = match.end()
            else:
                location = match.start()
            distance = abs(position - location)
            word = match.group()
            if word != prefix and fuzzy_match(prefix, word):
                candidates.append(Candidate(distance, word))

        for default_candidate in default_candidates:
            if not any(default_candidate.text == candidate.text for candidate in candidates):
                candidates.append(default_candidate)
        candidates.sort(key=self.get_distance)
        candidates = [candidate.text for candidate in candidates]
        if candidates:
            candidates.append(prefix)
        return uniq(candidates)

    def populate_candidates(self, prefix):
        settings_name, _ = os.path.splitext(os.path.basename(self.view.settings().get('syntax')))
        default_settings = sublime.load_settings("alternative_autocompletion.sublime-settings")
        default_candidates = default_settings.get(settings_name, [])

        user_settings = sublime.load_settings(settings_name + ".sublime-settings")
        user_candidates = user_settings.get('autocomplete', [])

        merge = user_settings.get('merge', {}).get(settings_name)
        if not merge:
            merge = default_settings.get('merge', {}).get(settings_name)
        if merge:
            for merge_settings_name in merge:
                default_candidates += default_settings.get(settings_name, [])
                merge_settings = sublime.load_settings(merge_settings_name + ".sublime-settings")
                user_candidates += merge_settings.get('autocomplete', [])

        # some languages, like "HTML 5", map to another language, like "PHP"
        # so if default_candidates is a str/unicode, look for that list
        while isinstance(default_candidates, str):
            settings_name = default_candidates
            default_candidates = default_settings.get(settings_name)
            if not user_candidates:
                user_settings = sublime.load_settings(settings_name + ".sublime-settings")
                user_candidates = user_settings.get('autocomplete')

        if default_candidates:
            candidates = [Candidate(self.view.size(), word) for word in default_candidates if fuzzy_match(prefix, word)]
        else:
            candidates = []

        # now merge user settings
        if user_candidates:
            candidates.extend([Candidate(self.view.size(), word) for word in user_candidates if fuzzy_match(prefix, word)])

        return candidates
