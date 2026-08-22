import itertools
import pytest

from linux_mint_script import Args


BOOL = [True, False]


@pytest.mark.parametrize(
    "release, debug, x64, x86, base64, default_xor, xor_key, "
    "both_encoding, hardcode, input, output, resource, header, "
    "encode_list, dropper_write, keep_log, log_number, logging_output, "
    "no_encode, no_compile, no_decode, test_output",
    itertools.product(
        BOOL,               # release
        BOOL,               # debug
        BOOL,               # x64
        BOOL,               # x86
        BOOL,               # base64
        BOOL,               # default_xor
        range(256),         # xor_key: 0-255
        BOOL,               # both_encoding
        BOOL,               # hardcode
        [None],             # input
        [None],             # output
        [None],             # resource
        [None],             # header
        [None],             # encode_list
        [None],             # dropper_write
        BOOL,               # keep_log
        range(41),          # log_number: 0-40
        [None],             # logging_output
        BOOL,               # no_encode
        BOOL,               # no_compile
        BOOL,               # no_decode
        BOOL,               # test_output
    ),
)
def test_revise_args(
    release,
    debug,
    x64,
    x86,
    base64,
    default_xor,
    xor_key,
    both_encoding,
    hardcode,
    input,
    output,
    resource,
    header,
    encode_list,
    dropper_write,
    keep_log,
    log_number,
    logging_output,
    no_encode,
    no_compile,
    no_decode,
    test_output,
):
    args = Args(
        release=release,
        debug=debug,
        x64=x64,
        x86=x86,
        base64=base64,
        default_xor=default_xor,
        xor_key=xor_key,
        both_encoding=both_encoding,
        hardcode=hardcode,
        input=input,
        output=output,
        resource=resource,
        header=header,
        encode_list=encode_list,
        dropper_write=dropper_write,
        keep_log=keep_log,
        log_number=log_number,
        logging_output=logging_output,
        no_encode=no_encode,
        no_compile=no_compile,
        no_decode=no_decode,
        test_output=test_output,
    )

    revise_args(args)
