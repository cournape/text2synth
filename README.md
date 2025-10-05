# text2synth, a PoC of using LLM to tweak synth patches

This is a PoC to tweak synths patches based on natural languages. This is also
an excuse to play a bit MCP, python libraries for LLM and have a bit of
fun.

I have only a couple of hours to build this PoC for AI tinkerers Japan.

## TODO

- [ ] Must
  - [x] Connect to HW synth w/ python + USB midi interface, send/rec msg
  - [ ] Dump current patch or settings -> not possible through MIDI
  - [x] manually change one setting through midi
  - [x] build a full map of CC implementation
  - [x] Use LLM as patch creator, no tooling
    - [x] update JU-06A, factory reset, backup factory reset and download sets
    of patch files
    - [x] Manually create a pydantic class representing a patch w/ proper range
    - [ ] Map patch format to CC, and function to apply patch through mido, and
    check a few examples by ear
    - [ ] try LLM prompting to create basic text2patch
  - [ ] test exposing MCP server as set of functions, one per CC
  - [ ] integrate w/ LLM and try, e.g. create pad or lead
- [ ] good to have
  - [ ] find bank patches and use it for prompting
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

## Patches

No patch is included in the source code for copyright reasons.

### Factory patch banks

To download the factory patches, simply follow the instructions to backup your
JU-06A, and move them into the directory patches/factory-banks.

Patches 1 to 64 are meant to be used in JUNO 60 mode, and the patches 65 to 128
in JU 106 mode.

### Other patches

The [Ultimate patch set](https://rekkerd.org/patches/plug-in/ju-06a/) gives a few more 100s of patches to use for prompting, etc.
