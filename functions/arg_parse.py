override_security_check_wfa = False
override_security_check_integrity = False

def arg_parse(argv):
    global override_security_check_wfa, override_security_check_integrity
    print("Parsing arguments...")
    print(f"Arguments: {argv}")
    exclude_flags = {
        "security_check_wfa": "override_security_check_wfa",
        "security_check_integrity": "override_security_check_integrity"
    }

    for i, arg in enumerate(argv[1:]):
        if arg == "--exclude" and i + 2 <= len(argv):
            flags_str = argv[i + 2]
            flags_list = [f.strip() for f in flags_str.split(",")]
            for flag in flags_list:
                if flag in exclude_flags:
                    globals()[exclude_flags[flag]] = True
                else:
                    print(f"[WARN] Unknown flag: {flag}")

