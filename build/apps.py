"""Things outside the Plasma stack: font rendering, VS Code, Firefox chrome.

Each of these has its own idea of where a theme lives, so none of them can be
driven from the colour scheme: the palette is re-emitted in the format each one
expects. They all come from the same tokens, so they cannot drift.
"""
import json

FONTS_CONF = '''<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd">
<!-- Neon Noir font rendering. Slight hinting and subpixel order to match the
     design's type: the UI face is a humanist sans at small sizes, and full
     hinting distorts its stems. -->
<fontconfig>
  <match target="font">
    <edit name="antialias" mode="assign"><bool>true</bool></edit>
    <edit name="hinting" mode="assign"><bool>true</bool></edit>
    <edit name="hintstyle" mode="assign"><const>hintslight</const></edit>
    <edit name="rgba" mode="assign"><const>rgb</const></edit>
    <edit name="lcdfilter" mode="assign"><const>lcddefault</const></edit>
    <edit name="autohint" mode="assign"><bool>false</bool></edit>
  </match>

  <!-- Keep bitmap fonts out; they ruin the type at fractional scaling. -->
  <selectfont><rejectfont><pattern>
    <patelt name="scalable"><bool>false</bool></patelt>
  </pattern></rejectfont></selectfont>

  <alias><family>sans-serif</family><prefer><family>@UI@</family></prefer></alias>
  <alias><family>sans</family><prefer><family>@UI@</family></prefer></alias>
  <alias><family>monospace</family><prefer><family>@MONO@</family></prefer></alias>
  <alias><family>system-ui</family><prefer><family>@UI@</family></prefer></alias>
</fontconfig>
'''


def vscode_theme(T, ANSI, THEME_NAME):
    A = ANSI
    ui = {
        'editor.background': T['surface.view'],
        'editor.foreground': T['text.normal'],
        'editorLineNumber.foreground': T['text.disabled'],
        'editorLineNumber.activeForeground': T['accent.cyan'],
        'editor.lineHighlightBackground': T['surface.alt'],
        'editor.selectionBackground': T['selection.bg'],
        'editor.selectionHighlightBackground': T['accent.cyan.ghost'],
        'editor.findMatchBackground': T['status.neutral.ghost'],
        'editor.findMatchHighlightBackground': T['accent.cyan.ghost'],
        'editorCursor.foreground': T['accent.cyan'],
        'editorWhitespace.foreground': T['border.hairline'],
        'editorIndentGuide.background1': T['border.hairline'],
        'editorIndentGuide.activeBackground1': T['border.float'],
        'editorBracketMatch.background': T['accent.cyan.ghost'],
        'editorBracketMatch.border': T['accent.cyan.dim'],
        'editorGutter.modifiedBackground': T['status.neutral'],
        'editorGutter.addedBackground': T['status.positive'],
        'editorGutter.deletedBackground': T['status.negative'],
        'editorError.foreground': T['status.negative'],
        'editorWarning.foreground': T['status.neutral'],
        'editorInfo.foreground': T['accent.cyan'],

        'activityBar.background': T['surface.window'],
        'activityBar.foreground': T['text.normal'],
        'activityBar.inactiveForeground': T['text.dim'],
        'activityBar.activeBorder': T['accent.cyan'],
        'activityBarBadge.background': T['accent.cyan'],
        'activityBarBadge.foreground': T['text.oncolor'],

        'sideBar.background': T['surface.window'],
        'sideBar.foreground': T['text.dim'],
        'sideBar.border': T['border.hairline'],
        'sideBarSectionHeader.background': T['surface.window'],
        'sideBarSectionHeader.foreground': T['accent.cyan'],
        'sideBarTitle.foreground': T['text.dim'],

        'list.activeSelectionBackground': T['selection.bg'],
        'list.activeSelectionForeground': T['selection.fg'],
        'list.inactiveSelectionBackground': T['surface.selected'],
        'list.hoverBackground': T['surface.hover'],
        'list.highlightForeground': T['accent.cyan'],

        'editorGroupHeader.tabsBackground': T['surface.window'],
        'tab.activeBackground': T['surface.view'],
        'tab.activeForeground': T['text.normal'],
        'tab.activeBorderTop': T['accent.cyan'],
        'tab.inactiveBackground': T['surface.window'],
        'tab.inactiveForeground': T['text.dim'],
        'tab.border': T['border.hairline'],

        'titleBar.activeBackground': T['titlebar.active'],
        'titleBar.activeForeground': T['text.normal'],
        'titleBar.inactiveBackground': T['titlebar.inactive'],
        'titleBar.inactiveForeground': T['text.title.inactive'],
        'titleBar.border': T['border.hairline'],

        'statusBar.background': T['surface.window'],
        'statusBar.foreground': T['text.dim'],
        'statusBar.border': T['border.hairline'],
        'statusBar.noFolderBackground': T['surface.window'],
        'statusBarItem.remoteBackground': T['accent.cyan.deep'],
        'statusBarItem.remoteForeground': T['selection.fg'],

        'panel.background': T['surface.view'],
        'panel.border': T['border.hairline'],
        'panelTitle.activeForeground': T['accent.cyan'],
        'panelTitle.activeBorder': T['accent.cyan'],
        'panelTitle.inactiveForeground': T['text.dim'],

        'input.background': T['surface.view'],
        'input.foreground': T['text.normal'],
        'input.border': T['border.hairline'],
        'input.placeholderForeground': T['text.disabled'],
        'focusBorder': T['accent.cyan'],
        'inputOption.activeBorder': T['accent.cyan'],

        'button.background': T['accent.cyan'],
        'button.foreground': T['text.oncolor'],
        'button.hoverBackground': T['accent.cyan.hover'],
        'button.secondaryBackground': T['surface.raised'],
        'button.secondaryForeground': T['text.normal'],
        'badge.background': T['accent.cyan'],
        'badge.foreground': T['text.oncolor'],

        'dropdown.background': T['surface.raised'],
        'dropdown.border': T['border.hairline'],
        'dropdown.foreground': T['text.normal'],

        'menu.background': T['surface.float'],
        'menu.foreground': T['text.normal'],
        'menu.selectionBackground': T['surface.hover'],
        'menu.border': T['border.float'],
        'menubar.selectionBackground': T['surface.hover'],

        'quickInput.background': T['surface.float'],
        'quickInputList.focusBackground': T['selection.bg'],
        'editorWidget.background': T['surface.float'],
        'editorWidget.border': T['border.float'],
        'editorSuggestWidget.selectedBackground': T['selection.bg'],
        'peekViewEditor.background': T['surface.alt'],

        'scrollbarSlider.background': T['border.float'] + '66',
        'scrollbarSlider.hoverBackground': T['accent.cyan.dim'] + '99',
        'scrollbarSlider.activeBackground': T['accent.cyan'] + 'cc',

        'widget.border': T['border.hairline'],
        'contrastBorder': T['border.hairline'],
        'foreground': T['text.normal'],
        'descriptionForeground': T['text.dim'],
        'errorForeground': T['status.negative'],
        'textLink.foreground': T['accent.indigo'],
        'textLink.activeForeground': T['accent.cyan'],

        'terminal.background': T['surface.void'],
        'terminal.foreground': T['text.normal'],
        'terminalCursor.foreground': T['accent.cyan'],
        'terminal.selectionBackground': T['selection.bg'],
    }
    for name, key in (('Black', 'black'), ('Red', 'red'), ('Green', 'green'),
                      ('Yellow', 'yellow'), ('Blue', 'blue'), ('Magenta', 'magenta'),
                      ('Cyan', 'cyan'), ('White', 'white')):
        ui[f'terminal.ansi{name}'] = A[key]
        ui[f'terminal.ansiBright{name}'] = A['br' + key]

    def style(scopes, colour, italic=False):
        s = {'scope': scopes, 'settings': {'foreground': colour}}
        if italic:
            s['settings']['fontStyle'] = 'italic'
        return s

    tokens = [
        style(['comment', 'punctuation.definition.comment'], T['text.disabled'], True),
        style(['string', 'string.quoted', 'punctuation.definition.string'], A['brgreen']),
        style(['constant.character.escape', 'string.regexp'], A['brcyan']),
        style(['constant.numeric', 'constant.language', 'constant.other'], A['bryellow']),
        style(['keyword', 'storage.type', 'storage.modifier'], A['brmagenta']),
        style(['keyword.control', 'keyword.operator.new'], A['brmagenta']),
        style(['keyword.operator'], A['white']),
        style(['entity.name.function', 'support.function', 'meta.function-call'], A['brblue']),
        style(['variable', 'variable.other', 'meta.definition.variable'], T['text.normal']),
        style(['variable.parameter'], A['blue'], True),
        style(['entity.name.type', 'entity.name.class', 'support.type', 'support.class'],
              A['bryellow']),
        style(['entity.name.tag'], A['brmagenta']),
        style(['entity.other.attribute-name'], A['brcyan']),
        style(['meta.preprocessor', 'keyword.control.directive'], A['brcyan']),
        style(['punctuation'], T['text.dim']),
        style(['invalid', 'invalid.illegal'], T['status.negative']),
        style(['markup.heading'], A['brcyan']),
        style(['markup.bold'], T['text.normal']),
        style(['markup.inserted'], T['status.positive']),
        style(['markup.deleted'], T['status.negative']),
    ]
    return json.dumps({
        'name': THEME_NAME,
        '$schema': 'vscode://schemas/color-theme',
        'type': 'dark',
        'semanticHighlighting': True,
        'colors': ui,
        'tokenColors': tokens,
    }, indent=2) + '\n'


FIREFOX_CHROME = '''/* Neon Noir — Firefox chrome.
   Deliberately narrow: browser chrome selectors change between releases, so
   this restyles the surfaces and the focus ring and leaves layout alone.
   Needs toolkit.legacyUserProfileCustomizations.stylesheets = true, which
   install.sh writes into the profile's user.js. */
:root {
  --nn-void:   @VOID@;
  --nn-window: @WINDOW@;
  --nn-view:   @VIEW@;
  --nn-raised: @RAISED@;
  --nn-hover:  @HOVER@;
  --nn-hair:   @HAIR@;
  --nn-text:   @TEXT@;
  --nn-dim:    @DIM@;
  --nn-cyan:   @CYAN@;

  --toolbar-bgcolor: var(--nn-window) !important;
  --toolbar-color: var(--nn-text) !important;
  --tab-selected-bgcolor: var(--nn-raised) !important;
  --lwt-accent-color: var(--nn-window) !important;
  --arrowpanel-background: var(--nn-float, var(--nn-raised)) !important;
  --arrowpanel-color: var(--nn-text) !important;
  --arrowpanel-border-color: var(--nn-hair) !important;
  --focus-outline-color: var(--nn-cyan) !important;
}

#navigator-toolbox {
  background: var(--nn-window) !important;
  border-bottom: 1px solid var(--nn-hair) !important;
}

#TabsToolbar, #nav-bar, #PersonalToolbar {
  background: transparent !important;
  box-shadow: none !important;
}

/* An active tab is a raised surface with a 2px accent rule, the same shape the
   rest of the theme uses for a selected item. */
.tabbrowser-tab .tab-background {
  border-radius: 7px !important;
  border: none !important;
  box-shadow: none !important;
}
.tabbrowser-tab[selected] .tab-background {
  background: var(--nn-raised) !important;
  border-bottom: 2px solid var(--nn-cyan) !important;
  border-radius: 7px 7px 0 0 !important;
}
.tabbrowser-tab:not([selected]):hover .tab-background {
  background: var(--nn-hover) !important;
}
.tabbrowser-tab .tab-label { color: var(--nn-dim) !important; }
.tabbrowser-tab[selected] .tab-label { color: var(--nn-text) !important; }

#urlbar-background, #searchbar {
  background: var(--nn-view) !important;
  border: 1px solid var(--nn-hair) !important;
  border-radius: 7px !important;
}
#urlbar[focuswithin] > #urlbar-background {
  border-color: var(--nn-cyan) !important;
  box-shadow: none !important;
}
#urlbar-input, #urlbar .urlbar-input { color: var(--nn-text) !important; }

.urlbarView-row[selected] > .urlbarView-row-inner,
.urlbarView-row:hover > .urlbarView-row-inner {
  background: var(--nn-hover) !important;
  border-radius: 6px !important;
}

toolbarbutton .toolbarbutton-icon { border-radius: 6px !important; }
#sidebar-box, #sidebar-header {
  background: var(--nn-window) !important;
  color: var(--nn-text) !important;
}
'''

FIREFOX_CONTENT = '''/* Neon Noir — stop the white flash on Firefox's own blank pages. */
@-moz-document url("about:blank"), url("about:newtab"), url("about:home"),
               url("about:privatebrowsing") {
  :root, body { background-color: @VOID@ !important; }
}
'''

VSCODE_PACKAGE = {
    'name': 'neon-noir-theme',
    'displayName': '@NAME@',
    'description': 'Neon noir: cyan and magenta on blue-black',
    'version': '1.0.0',
    'publisher': 'george',
    'engines': {'vscode': '^1.70.0'},
    'categories': ['Themes'],
    'contributes': {
        'themes': [{
            'label': '@NAME@',
            'uiTheme': 'vs-dark',
            'path': './themes/neon-noir-color-theme.json',
        }],
    },
}


def build(T, ANSI, DIST, THEME_ID, THEME_NAME, UI_FONT, MONO_FONT):
    out = []

    fc = DIST / 'fontconfig'
    fc.mkdir(parents=True, exist_ok=True)
    (fc / 'fonts.conf').write_text(
        FONTS_CONF.replace('@UI@', UI_FONT).replace('@MONO@', MONO_FONT))
    out.append('fontconfig/fonts.conf')

    ext = DIST / 'vscode' / 'neon-noir-theme'
    (ext / 'themes').mkdir(parents=True, exist_ok=True)
    (ext / 'package.json').write_text(
        json.dumps(VSCODE_PACKAGE, indent=2).replace('@NAME@', THEME_NAME) + '\n')
    (ext / 'themes' / 'neon-noir-color-theme.json').write_text(
        vscode_theme(T, ANSI, THEME_NAME))
    out.append('vscode/neon-noir-theme/  (package.json, colour theme)')

    ff = DIST / 'firefox'
    ff.mkdir(parents=True, exist_ok=True)
    subs = {'@VOID@': T['surface.void'], '@WINDOW@': T['surface.window'],
            '@VIEW@': T['surface.view'], '@RAISED@': T['surface.raised'],
            '@HOVER@': T['surface.hover'], '@HAIR@': T['border.hairline'],
            '@TEXT@': T['text.normal'], '@DIM@': T['text.dim'],
            '@CYAN@': T['accent.cyan']}
    for name, tmpl in (('userChrome.css', FIREFOX_CHROME),
                       ('userContent.css', FIREFOX_CONTENT)):
        s = tmpl
        for k, v in subs.items():
            s = s.replace(k, v)
        (ff / name).write_text(s)
    (ff / 'user.js').write_text(
        '// Added by Neon Noir: without this Firefox ignores userChrome.css.\n'
        'user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);\n')
    out.append('firefox/userChrome.css, userContent.css, user.js')
    return out
