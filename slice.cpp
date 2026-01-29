#include <iostream>
using namespace std;

class Slice {
	private:
		string* text;
		int start;
		int end;
	public:
		Slice(string* txt, int st, int en) {
			text = txt;
			start = st;
			end = en;
		};
		friend ostream& operator <<(ostream&, const Slice&);
	
};

ostream& operator <<(ostream& out, const Slice& v) {
	out << v.text->substr(v.start, v.end - v.start);
	return out;
};

int main() {
	string s = "Hello there! This is Nickhil Sethi";
	Slice v = Slice(&s, 0, 7);
	cout << v << endl;
	return 0;
}
