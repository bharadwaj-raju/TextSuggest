#ifndef INDEX_H
#define INDEX_H

class Index {
public:
	Index(int value, int maxvalue) {
		this->value = value;
		this->maxvalue =  maxvalue;
	};
	~Index() {};

	int value;
	int maxvalue;

	int normalized(int val) {
		if (val < 0) {
			return 0;
		}
		if (val > maxvalue) {
			return maxvalue;
		} else {
			return val;
		}
	};

	void set(int val) {
		value = normalized(val);
	};

	int get() {
		return value;
	};

	void setMax(int newmax) {
		maxvalue = newmax;
	};

	int getMax() {
		return maxvalue;
	};

};

#endif // INDEX_H