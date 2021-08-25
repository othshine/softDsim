import json

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from app.src.domain.decision_tree import Scenario, Decision


def index(request):
    s = Scenario()
    s.add(Decision("This is Question number one"))
    return render(request, "app/index.html")


def click_continue(request):
    print("CONTINUE")
    counter = int(request.GET.get("counter"))

    class DataObj(object):
        def __init__(self, header, text):
            self.header = header
            self.text = text

    data = [
        [DataObj("Welcome",
                 "You are the assistant of a project manager in a company that manufactures various multimedia products as an automotive supplier. You are now assigned to contribute to the decision making process."),
         DataObj("Story",
                 "A regular customer, a German car manufacturer, commissions their company to develop a car radio for a new model series. There are no special features to be considered for the development, it is quite an ordinary radio. All specifications are specified in detail by the car manufacturer. You are now to build this product and later put it into production."),
         DataObj("Task",
                 "The first step is to plan the project. You should first define the project life cycle, what kind of life cycle is it?")],
        [DataObj("Feedback",
                 "Unfortunately, the project manager can't understand your assessment very well. You should think about that again. Isn't there a life cycle that fits better to the described scenario?"),
         DataObj("Story",
                 "A regular customer, a German car manufacturer, commissions their company to develop a car radio for a new model series. There are no special features to be considered for the development, it is quite an ordinary radio. All specifications are specified in detail by the car manufacturer. You are now to build this product and later put it into production."),
         DataObj("Task", "In the next step, you should select a suitable project management model.")
         ],
        [
            DataObj("Feedback", "Good choice. The project manager is satisfied with your assistance."),
            DataObj("Expectations", "€37,500 have been released by management for the project. The project is not very complex and does not use any extraordinary technologies. However, it should be noted that the project, especially because it is so simple, needs to have a very high quality."),
            DataObj("Task", "Assemble a team that meets the requirements well.")
        ],
        [
            DataObj("Feedback", "Your team has been considered all right by the project manager, so you can go ahead with it."),
            DataObj("Scheduling", "The team was presented with the requirements document. All requirements and specifications are detailed and must now be implemented. "),
            DataObj("Task", "You should now create a schedule and indicate whether it is possible to create the radio by the desired time. At the same time, your schedule should include the planning of possible prototypes.")
        ],
        [
            DataObj("Request for Change", "Suddenly, the inquiring customer comes back with a change. A certain interface for cell phones has just been made public in a new version. The customer now wants this new version of the interface to be supported by the radio in order to be able to offer its customers a future-proof product."),
            DataObj("Task", "How do you respond to this request. Adjust all the parameters of the project that you consider necessary. Your suggestions will be discussed in a meeting with senior managers and the client in two days.")
        ]
    ]

    dj = [d.__dict__ for d in data[counter]]

    return HttpResponse(json.dumps(dj), content_type="application/json")
