/*
 * pimp_sample.hpp
 *
 *  Created on: 2011-3-6
 *      Author: reliu
 */

#ifndef PIMP_SAMPLE_HPP_
#define PIMP_SAMPLE_HPP_

struct impl;
class pimpl_sample
{
	impl* pimpl_;
	//boost::scoped_ptr<impl> pimpl_;
public:
	pimpl_sample();
	~pimpl_sample();
	void do_something();
};
#endif /* PIMP_SAMPLE_HPP_ */
