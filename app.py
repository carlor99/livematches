from flask import Flask, render_template, request
import main

app = Flask(__name__)

@app.route('/', methods=["GET"])
def home():
        matchlist = main.return_matchlist()
        return render_template('index.html',
                                matchlist=matchlist
                            )

@app.route('/clear_filter', methods=["POST"])
def clear_filter():
        matchlist = main.return_matchlist()
        return render_template('index.html',
                                matchlist=matchlist
                            )

@app.route('/filter_00', methods=['POST'])
def filter_00():
    matchlist = main.return_matchlist()
    # Filter matches with 0-0 score
    filtered_matches = [match for match in matchlist if match.homescore == '0' and match.awayscore == '0']
    return render_template('index.html', matchlist=filtered_matches)

@app.route('/filter_00_plus70', methods=['POST'])
def filter_00_plus70():
    matchlist = main.return_matchlist()
    # Filter matches with 0-0 score
    filtered_matches = [match for match in matchlist if match.homescore == '0' and match.awayscore == '0' and match.time >= 70]
    return render_template('index.html', matchlist=filtered_matches)

if __name__ == '__main__':
    app.run(debug=True)
