#include <iostream>
using namespace std;

class Slice {
	private:
		const string* text;
		int start;
		int end;
	public:
		Slice(const string* txt, int st, int en) {
			// error checking here
			text = txt;
			start = st;
			end = en;
		};
	
		Slice(const Slice& sl) {
			text = sl.text;
			start = sl.start;
			end = sl.end;
		};	
		
		const bool operator ==(const Slice& sl) {
			if (this->text != sl.text) {
				return false;
			}
			if (this->start != sl.start) {
				return false;
			}
			if (this->end != sl.end) {
				return false;
			}
			return true;
			
		};

		const Slice& operator =(const Slice& sl) {
			if (*this == sl) {
				return *this;
			}

			text = sl.text;
			start = sl.start;
			end = sl.end;

			return *this;
		};
		
		string get_text() const {
			return text->substr(start, end - start);
		};

		friend ostream& operator <<(ostream&, const Slice&);
		friend const Slice merge(const Slice&, const Slice&);
	
};

ostream& operator <<(ostream& out, const Slice& v) {
	out << v.get_text();
	return out;
};

const Slice merge(const Slice& sl1, const Slice& sl2) {
	// assert same text
	int start = min(sl1.start, sl2.start);
	int end = max(sl1.end, sl2.end);
	return Slice(sl1.text, start, end);
};

vector<Slice> analyze_text(string& text, int slice_length) {
	vector<Slice> ret;
	for (int i = 0; i < text.length() - slice_length; i++) {
		ret.push_back(Slice(&text, i, i+slice_length));
	}
	return ret;
}

int main() {
	string s = "Hello there! This is Nickhil Sethi";
	vector<Slice> spans = analyze_text(s, 3);
	for(auto s : spans) {
		cout << s << endl;
	}
	return 0;
}
