#!/usr/bin/env python3
import argparse
import logging
import sys
import time

import mido


DEFAULT_MIDI_IN = DEFAULT_MIDI_OUT = "USB MIDI Interface"
LOGGER = logging.getLogger(__name__)


def list_ports_cli(args):
    print("MIDI Input Ports:")
    for name in mido.get_input_names():
        print("  ", name)

    print("\nMIDI Output Ports:")
    for name in mido.get_output_names():
        print("  ", name)


def control_change_cli(args):
    outport_name = args.midi_out
    number = args.cc_number
    value = args.cc_value

    LOGGER.debug("Sending CC %d with value %d", number, value)

    with mido.open_output(outport_name) as outport:
        LOGGER.debug("Ready to use port")

        msg = mido.Message('control_change', control=number, value=value)
        outport.send(msg)


def main():
    logging.basicConfig(level=logging.DEBUG,
                        format="%(levelname)s:%(module)s.%(funcName)s: %(message)s")

    parser = argparse.ArgumentParser(description="Simple MIDI CLI")
    parser.add_argument("--midi-in", type=str, default=DEFAULT_MIDI_IN,
                        help="MIDI input device")
    parser.add_argument("--midi-out", type=str, default=DEFAULT_MIDI_OUT,
                        help="MIDI output device")

    subparsers = parser.add_subparsers(dest="command", required=True)

    cc_parser = subparsers.add_parser("control-change", aliases=["cc"],
                                      help="Send a MIDI control change message")
    cc_parser.add_argument("cc_number", type=int, help="Control change number")
    cc_parser.add_argument("cc_value", type=int, help="Control change value")
    cc_parser.add_argument("--channel", type=int, default=1,
                           help="MIDI channel (default: 1)")
    cc_parser.set_defaults(func=control_change_cli)

    list_ports_parser = subparsers.add_parser("list-ports",
                                      help="list ports")
    list_ports_parser.set_defaults(func=list_ports_cli)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        print("No operation implemented for this command yet.")
        sys.exit(-1)

if __name__ == "__main__":
    main()

