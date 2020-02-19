# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 21:32:47 2018

@author: nik
"""
from haversine import haversine

donor_hospital = (45.7597, 4.8422)
acceptor_hospital = (48.8567, 2.3508)


height_difference= (donorHeight -acceptorHeight)/donorHeight
#Scaled to be less than 1

weight_difference= (donorWeight -acceptorWeight)/donorWeight


min=3


#donor represents a dictionary with all the donor data
#Once donor dies, put in differnt values for Organ Request to test for matches

if(organRequest=="heart"):
    if("infect" in donor["patientCardiovascular"]):

        print("Donor can't donate a heart")
        exit()
        #THIS PATIENT'S HEART IS USELESS
        else
        for acceptor in acceptor_li:
            if (donor["bloodType"]== acceptor["bloodType"]):
                height_difference= (acceptor["height"]-donor["height"])/acceptor["height"]
                weight_difference= (acceptor["weight"]-donor["weight"])/acceptor["weight"]
                age_difference= (acceptor["age"]-donor["age"])/acceptor["age"]
                distance_difference= haversine(donor_hospital, acceptor_hospital)



                sum=distance_difference+ height_difference + weight_difference + age_difference

                if(sum<min):
                    min=sum
                    best_acceptor= acceptor["name"]

        print(best_acceptor)


if(organRequest=="lungs"):

    if("infect" in donor["respiratory"] or donor["smoking"]=="yes")
        print("Donor can't donate a lung")
        exit()
        #THIS PATIENT'S Lung IS USELESS
    if (donor["bloodType"]!= acceptor["bloodType"]):

        for acceptor in acceptor_li:

            height_difference= (acceptor["height"]-donor["height"])/acceptor["height"]
            weight_difference= (acceptor["weight"]-donor["weight"])/acceptor["weight"]
            age_difference= (acceptor["age"]-donor["age"])/acceptor["age"]

            distance_difference= haversine(donor_hospital, acceptor_hospital)


            sum=distance_difference+ height_difference + weight_difference + age_difference

            if(sum<min):
                min=sum
                best_acceptor= acceptor["name"]

        print(best_acceptor)


if(organRequest=="kidney"):

    if(donor["kidneyDisease"]=="yes" or donor["urine"]=="yes" or donor["Polyuria"]== "yes"):
        print("Donor can't donate a lung")
        exit()
        #THIS PATIENT'S Lung IS USELESS

    if( donor["Polyuria"]== acceptor["Polyuria"]):

        for acceptor in acceptor_li:

            height_difference= (acceptor["height"]-donor["height"])/acceptor["height"]
            weight_difference= (acceptor["weight"]-donor["weight"])/acceptor["weight"]
            age_difference= (acceptor["age"]-donor["age"])/acceptor["age"]

            distance_difference= haversine(donor_hospital, acceptor_hospital)


            sum=distance_difference+ height_difference + weight_difference + age_difference

            if(sum<min):
                min=sum
                best_acceptor= acceptor["name"]

        print(best_acceptor)
