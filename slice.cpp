#include <iostream>
using namespace std;

class Slice {
	private:
		string* text;
		int start;
		int end;
	public:
		Slice(string* txt, int st, int en) {
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
		
		const Slice& operator =(const Slice& sl) {
			// if (*this == sl) {
			//	return *this;
			//}

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

int main() {
	string s = "Hello there! This is Nickhil Sethi";
	Slice v = Slice(&s, 0, 7);
	Slice w = Slice(&s, 7, 14);
	cout << merge(v,w) << endl;
	return 0;
}
