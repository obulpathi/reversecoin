def uint256_from_compact(c):
    nbytes = (c >> 24) & 0xFF
    v = (c & 0xFFFFFF) << (8 * (nbytes - 3))
    return v

def compact_from_uint256(v):
    v_hex = hex(v)
    if int(v_hex[:4], 16) > 127:
        v_hex = v_hex[:2] + "00" + v_hex[2:]
    nbytes = 0xFF & ((len(v_hex)-3)//2)
    nbytes = (nbytes << 8) | (int(v_hex[2:4], 16) & 0xFF)
    nbytes = (nbytes << 8) | (int(v_hex[4:6], 16) & 0xFF)
    nbytes = (nbytes << 8) | (int(v_hex[6:8], 16) & 0xFF)
    return nbytes

compacts = [0x0500ffff, 0x0600ffff, 0x0700ffff]
for compact in compacts:
    target = uint256_from_compact(compact)
    new_compact = compact_from_uint256(target)
    print "Compact: ", compact, "Target: ", target, "New compact: ", new_compact
