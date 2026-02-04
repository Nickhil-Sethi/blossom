#include <iostream>
using namespace std;

#include "document_explorer.h"

const bool DocumentExplorer::operator ==(const DocumentExplorer& doc_exp) {
	if this->text == doc_exp.text {
		return true;
	}
	return false;
};

DocumentExplorer& DocumentExplorer::operator =(const DocumentExplorer& doc_exp) {
	text = doc_exp.text;
	index();
};
