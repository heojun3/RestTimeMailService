from .office_time_calculator import calculate_rest_work_time
import argparse

if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(
            description="Calculate remaining office hours")
        parser.add_argument('email', type=str, help='Your Email Address')
        args = parser.parse_args()

        message = calculate_rest_work_time(args.email)
        print(message)
    except Exception as e:
        print(e)
