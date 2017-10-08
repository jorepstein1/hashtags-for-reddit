import praw
import flask
import datetime

reddit = praw.Reddit('main')
app = flask.Flask(__name__)

TIME_FORMAT = "%b %d, %H:%M:%S"

@app.route('/')
def index():

    num_submissions = 10
    subreddit = "all"
    recent_submissions = get_recent_submissions(num_submissions, subreddit)

    ret = ''
    ret += get_header(num_submissions, subreddit)
    ret += format_recent_submissions(recent_submissions)
    return ret

def get_header(num: int, subreddit: str):
    time = datetime.datetime.strftime(datetime.datetime.now(), TIME_FORMAT)
    header = '<h1>{} most recent submissions as of {}:<h1>'.format(num,
                                                                       time)
    header += '<pre>&#9;</pre> Subreddit: {}<br>'.format(subreddit)
    return header

def get_recent_submissions(num: int, subreddit: str):
    subr = reddit.subreddit(subreddit)
    recent_submissions = [sub for sub in subr.new(limit=num)]
    return recent_submissions

def format_recent_submissions(recent_submissions):
    ret = ''
    for sub in recent_submissions:
        timestamp = datetime.datetime.fromtimestamp(sub.created)
        time = datetime.datetime.strftime(timestamp, TIME_FORMAT)
        ret += "Title: {}<br> Subreddit: {}<br>Time posted: {}<br><br>".format(
            sub.title, sub.subreddit, time)
    return ret
    # return "<br>".join(dir(recent_submissions[0]))

if __name__ == '__main__':
    app.run(host='192.168.0.108', port=5000, debug=True)