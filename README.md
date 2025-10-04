# text2synth, a PoC of using LLM to tweak synth patches

This is a PoC to tweak synths patches based on natural languages. This is also
an excuse to play a bit MCP, python libraries for LLM and have a bit of
fun.

I have only a couple of hours to build this PoC for AI tinkerers Japan.
I focus on interfacing with the Roland boutique JU-O6A: it is battery-powered,
which is nice for the demo, and is simple enough I can cover all of it easily.
Some cons of this synth: lack of SysEx, and inability to dump patch. But for the
demo it should do.

## TODO

- [ ] Must
  - [x] Connect to HW synth w/ python + USB midi interface, send/rec msg
  - [ ] Dump current patch or settings -> not possible through MIDI
  - [x] manually change one setting through midi
  - [ ] build a full map of CC implementation
  - [ ] build a basic dispatch function taking to control arbitrary message +
  CLI for testing
    - [ ] test using MIDI keyboard
    - [ ] test arpegiator
  - [ ] test exposing MCP server as a single function dispatch
  - [ ] integrate w/ LLM
  - [ ] test exposing MCP server as a a set of ctions
- [ ] good to have
  - [ ] find bank patches and link description to
  - [ ] try with one effect, e.g. volante or reverb or analog heat

## Links

- [Reddit
video](https://www.reddit.com/r/synthesizers/comments/ndmeze/everything_in_its_right_place_roland_ju06a_patch)
of everything in its place patch (video only)
- [Patch list](https://sunshine-jones.com/ju-06-ju-06a-patch-exchange/) for
both 60 and 106 modes w/ the numbering logic
- [Some 2024 ICML paper](https://ctag.media.mit.edu/) that I found when looking
  for text2synth. Have not read the paper yet, but seems to be using a virtual
synth to have a loop text -> synth audio -> refine. Our goal here is much more
mundane.
