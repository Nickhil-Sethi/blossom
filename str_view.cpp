#include <iostream>
using namespace std;

class View {
	private:
		string* text;
		int start;
		int end;
	public:
		View(string* txt, int st, int en) {
			text = txt;
			start = st;
			end = en;
		};
		friend ostream& operator <<(ostream&, const View&);
	
};

ostream& operator <<(ostream& out, const View& v) {
	out << v.text->substr(v.start, v.end - v.start);
	return out;
};

int main() {
	string s = "Hello there! This is Nickhil Sethi";
	View v = View(&s, 0, 7);
	cout << v << endl;
	return 0;
}
