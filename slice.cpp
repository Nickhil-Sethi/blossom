#include <iostream>
#include <string> 
#include <set>
#include <algorithm>
using namespace std;

#include "slice.h"
string Slice::get_text() const {
	return text->substr(start, end - start);
};

string Slice::hash() const {
	return get_text() + to_string(start) + ":" + to_string(end);
}
ostream& operator <<(ostream& out, const Slice& v) {

	int display_start = max(0, v.start-10);
	int text_length = v.text->length();
	int display_end = min(text_length, v.end + 10);

	out << "begin: " << v.start << " end: " << v.end << endl;
	out << v.text->substr(display_start, v.start - display_start) << " [[" << v.get_text() << "]] " << v.text->substr(v.end, display_end - v.end);
	return out;
};

vector<Slice> deduplicate(vector<Slice> data) {
	set<string> hashes;
	string sl_hash;

	vector<Slice> ret;
	for (Slice sl : data) {
		sl_hash = sl.hash();
		if (hashes.find(sl_hash) == hashes.end()) {
			hashes.insert(sl_hash);
			ret.push_back(sl);
		}
	}
	return ret;
}

const Slice merge(const Slice& sl1, const Slice& sl2) {
	// assert same text
	int start = min(sl1.start, sl2.start);
	int end = max(sl1.end, sl2.end);
	return Slice(sl1.text, start, end);
};

int seek_whitespace(const string& text, int offset) {
	while(offset < text.length() && 
	     !(isspace(text[offset]))
	){ offset++; };

	return offset;
}

int seek_non_whitespace(const string& text, int offset) {
	while(offset < text.length() && 
	     isspace(text[offset])
	){ offset++; };

	return offset;
}

vector<Slice> analyze_text(const string& text, int slice_length) {
	vector<Slice> ret;

	int c = seek_non_whitespace(text, 0);
	int d = c;

	while (c < text.length() && d < text.length()) {

		while (d < text.length() && (d - c < slice_length)) {
			d = seek_whitespace(text, d);	
			ret.push_back(Slice(&text, c, d));
			d = seek_non_whitespace(text, d);
		};
		
		c = seek_whitespace(text, c);
		c = seek_non_whitespace(text, c);
	
		d = c;
	}
	return ret;
}

set<string> get_trigrams(const string& text) {
	set<string> trigrams;
	for (int i = 0; i + 2 < text.length(); i++) {
		trigrams.insert(text.substr(i, 3));
	}
	return trigrams;
}

void test_slice() {
	string s = "Hello there! This is Nickhil Sethi";
	vector<Slice> spans = analyze_text(s, 3);
	for(auto s : spans) {
		cout << s << endl;
	}
}
