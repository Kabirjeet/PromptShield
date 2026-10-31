SIGNATURES = {
    "prompt_override": [
        r"\bignore (all )?(previous|prior|earlier) instructions\b",
        r"\bdisregard (all )?(previous|prior|earlier) instructions\b",
        r"\boverride (the )?(previous|prior|system) instructions\b",
        r"\bforget (all )?(previous|prior) instructions\b",
    ],

    "system_prompt_extraction": [
        r"\breveal (your )?((system|hidden)\s+)*prompt\b",
        r"\bshow (me )?(your )?((system|hidden)\s+)*prompt\b",
        r"\bprint (your )?((system|hidden)\s+)*prompt\b",
        r"\bwhat is your ((system|hidden)\s+)*prompt\b",
    ],

    "role_manipulation": [
        r"\byou are now\b",
        r"\bact as (an? )?(unrestricted|unfiltered|different) ai\b",
        r"\bpretend (that )?you have no restrictions\b",
    ],

    "jailbreak": [
        r"\bignore your safety rules\b",
        r"\bdisable your safety\b",
        r"\bbypass your safety\b",
        r"\bbypass your restrictions\b",
        r"\bremove your restrictions\b",
    ],
}
