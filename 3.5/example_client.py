#!/usr/bin/env python
# encoding: utf8
#
# Copyright © Ruben Ruiz Torrubiano <ruben.ruiz at fh-krems dot ac dot at>,
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    1. Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#    3. Neither the name of the owner nor the names of its contributors may be
#       used to endorse or promote products derived from this software without
#       specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import grpc
import example_pb2
import example_pb2_grpc

if __name__ == '__main__':
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = example_pb2_grpc.CustomerServiceStub(channel)
        customer0 = example_pb2.Customer(forename='John', surname='Smith')

        response = stub.AddCustomer(customer0)
        print(f'First request response = {response.success}')

        if response.success:
            # add purchase for Smith
            purchase1 = example_pb2.Purchase(customer_id=response.customers[0].id, total_price=100.0, articles=[1, 2, 3])
            response1 = stub.SendPurchases(p for p in [purchase1])
            if response1.success:
                print(f'Purchase for customer {response.customers[0].id} was successful')
            else:
                print(f'Purchase for customer {response.customers[0].id} was not successful. Error message: {response1.error_message}')
            purchase2 = example_pb2.Purchase(customer_id=response.customers[0].id, total_price=70.0,
                                             articles=[5])
            response2 = stub.SendPurchases(p for p in [purchase2])
            if response2.success:
                print(f'Purchase for customer {response.customers[0].id} was successful')
            else:
                print(f'Purchase for customer {response.customers[0].id} was not successful. Error message: {response2.error_message}')
        customer0 = example_pb2.Customer(forename='John', surname='AAA')

        response = stub.AddCustomer(customer0)
        print(f'First request response = {response.success}')

        if response.success:
            # add purchase for Smith
            purchase1 = example_pb2.Purchase(customer_id=response.customers[0].id, total_price=100.0, articles=[1, 2, 3])
            response1 = stub.SendPurchases(p for p in [purchase1])
            if response1.success:
                print(f'Purchase for customer {response.customers[0].id} was successful')
            else:
                print(f'Purchase for customer {response.customers[0].id} was not successful. Error message: {response1.error_message}')
            purchase2 = example_pb2.Purchase(customer_id=response.customers[0].id, total_price=70.0,
                                             articles=[5])
            response2 = stub.SendPurchases(p for p in [purchase2])
            if response2.success:
                print(f'Purchase for customer {response.customers[0].id} was successful')
            else:
                print(f'Purchase for customer {response.customers[0].id} was not successful. Error message: {response2.error_message}')
        
        customer0 = example_pb2.Customer(forename='John', surname='AAb')

        response = stub.AddCustomer(customer0)
        print(f'First request response = {response.success}')

        if response.success:
            # add purchase for Smith
            purchase1 = example_pb2.Purchase(customer_id=response.customers[0].id, total_price=100.0, articles=[1, 2, 3])
            response1 = stub.SendPurchases(p for p in [purchase1])
            if response1.success:
                print(f'Purchase for customer {response.customers[0].id} was successful')
            else:
                print(f'Purchase for customer {response.customers[0].id} was not successful. Error message: {response1.error_message}')
            purchase2 = example_pb2.Purchase(customer_id=response.customers[0].id, total_price=30.0,
                                             articles=[5])
            response2 = stub.SendPurchases(p for p in [purchase2])
            if response2.success:
                print(f'Purchase for customer {response.customers[0].id} was successful')
            else:
                print(f'Purchase for customer {response.customers[0].id} was not successful. Error message: {response2.error_message}')
        
        response = stub.RichCustomers(response2)
        for customer in response:
            print(f'Customer {customer.id} Name: {customer.forename} {customer.surname} Total purchases: {sum([p.total_price for p in customer.purchases])} ')
