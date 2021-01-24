#!/usr/bin/env python3

from pullnrun import __version__
from pullnrun.main import get_args, load_plan_from_file, main, NO_PLAN

def entrypoint():
    args = get_args()
    if args.version:
        print(f'pullnrun {__version__}')
        return

    try:
        plan = load_plan_from_file(args.plan_file)
    except ValueError as e:
        print(str(e))
        exit(NO_PLAN)

    main(plan)

if __name__ == '__main__':
    entrypoint()
