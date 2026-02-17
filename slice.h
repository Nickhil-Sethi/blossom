#ifndef SLICE_H
#define SLICE_H

#include <iostream>
#include <vector>
#include <set>
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
		
		string get_text() const;
		string hash() const;
		friend ostream& operator <<(ostream&, const Slice&);
		friend const Slice merge(const Slice&, const Slice&);
	
};

const Slice merge(const Slice& sl1, const Slice& sl2);
vector<Slice> analyze_text(const string& text, int slice_length);
set<string> get_trigrams(const string& text);
vector<Slice> deduplicate(vector<Slice>);
#endif
