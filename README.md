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

- [ ] Simple stuff
  - [ ] Fix likely envelope bug
  - [ ] Implement reading state from JU-06A if feasible:
    - [ ] Confirm whether JU-06A can send CC or not. See
      [this page](https://chrissieviolin.wordpress.com/2015/11/20/reverse-engineering-the-roland-ju-06-synth)
      - [ ] Look at receive SysEx as well
      - [ ] Implement functionality to read state from HW
  - [ ] Basic video demo
  - [ ] Some tutorial to setup and use
  - [ ] basic doc
- [ ] Add support for other synths, using resources such as
[openmidi](https://github.com/Morningstar-Engineering/openmidi) or
[midi](https://github.com/pencilresearch/midi/)
  - [ ] Model code generator from text representation
  - [ ] Try it w/ Korg volca FM7 or some strymon pedals
- [ ] enhance MCP server:
  - [ ] Review Hugging face training to understand protocol nuance on
  discovery
  - [ ] Read from patch / save current state as patch
  - [ ] Play w/ resources to see if that helps
  - [ ] Tradeoff one dispatch tool vs set one for DCO, one for filter, etc.
- [ ] Improve claude desktop experience
  - [ ] MCP server improvements
- [ ] Improve the "AI part"
  - [ ] structured output w/ local LLM: try outlines w/ one of the local LLM I
  got recommended at AI tinkerers
  - [ ] Adding CLI chat, memory and what not
  - [ ] Try to "read" patch from picture
  - [ ] Experiment with audio2patch idea

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

The [Ultimate patch set](https://rekkerd.org/patches/plug-in/ju-06a/) gives a
few more 100s of patches to use for prompting, etc.
