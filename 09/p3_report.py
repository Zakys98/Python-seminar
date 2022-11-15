# The goal here is to load the file ‹zz.report.json› which contains
# a report about a bug in a C program, and print out a simple stack
# trace. You will be interested in the key ‹active stack› (near the
# end of the file) and its format. The output will be plain text:
# for each stack frame, print a single line in this format:
#
#     function_name at source.c:32

import json  # go for ‹load› (via io) or ‹loads› (via strings)


def report():
    with open('zz.report.json', 'r', encoding='utf-8-sig') as f:
        jsn = json.load(f)
        for stack in jsn['active stack']:
            print(f"{stack['symbol']} at {stack['location']}")


def test_main() -> None:
    def redirect_out() -> str:
        import sys
        from io import StringIO

        stdout = sys.stdout
        out = StringIO()
        sys.stdout = out

        report()

        sys.stdout = stdout
        return out.getvalue()

    output = redirect_out().split('\n')
    assert len(output) == 5 or len(output) == 6
    if len(output) == 6:
        assert not output[5].strip()

    assert output[0] == "void __dios::FaultBase::handler<__dios::Upcall<__dios::fs::VFS" \
                        "<__dios::ProcessManager<__dios::Fault<__dios::Scheduler" \
                        "<__dios::Base> > > > > >(_VM_Fault, _VM_Frame*, " \
                        "void (*)()) at /dios/include/dios/sys/fault.hpp:118"
    assert output[1] == "__dios_fault at /dios/src/arch/divm/fault.c:12"
    assert output[2] == "__assert_fail at /dios/src/libc/_PDCLIB/assert.c:21"
    assert output[3] == "main at test/lang-c/assert.c:6"
    assert output[4] == "__dios_start at /dios/src/libc/sys/start.cpp:102"


if __name__ == "__main__":
    test_main()
