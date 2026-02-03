#include <iostream>
using namespace std;

#include "slice.h"
string Slice::get_text() const {
	return text->substr(start, end - start);
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

void  test_slice() {
	string s = "Hello there! This is Nickhil Sethi";
	vector<Slice> spans = analyze_text(s, 3);
	for(auto s : spans) {
		cout << s << endl;
	}
}
