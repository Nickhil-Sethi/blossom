#ifndef DOC_EXP_H
#define DOC_EXP_H

#include <iostream>
using namespace std;

class DocumentExplorer {
	private:
		const string* text;
		virtual void index() = 0;
	public:
		DocumentExplorer(const string* doc_txt) {
			text = doc_txt;
		};
		
		DocumentExplorer(const DocumentExplorer& doc_exp) {
			text = doc_exp.text;
			index();
		};

		const bool operator ==(const DocumentExplorer& doc_exp);
		const DocumentExplorer& operator =(const DocumentExplorer& doc_exp);	
		
};

#endif
