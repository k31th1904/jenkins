#!/bin/bash


echo "Installing the first release ..."
echo ""
helm install apple-release1 --set service.port=8000 .
echo ""
echo "Installing the second release ..."
helm install apple-release2 --set service.port=9000 .
