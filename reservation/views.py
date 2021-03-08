import json
from datetime           import date

from django.shortcuts   import render
from django.http        import HttpResponse, JsonResponse
from django.views       import View
from django.db.models   import Q

from reservation.models import Reservation
from user.utils         import login_decorator

class ReservationListView(View):
    @login_decorator
    def get(self, request):
        try:
            user            = request.user
            reservations    = Reservation.objects.filter(~Q(status_id=1), user_id=user.id).select_related('accommodation').prefetch_related('accommodation__image_set')
            
            if not reservations:
                return JsonResponse({'message': 'NO_RESERVATION'}, status=200)

            upcoming_reservations   = []
            past_reservations       = []
            canceled_reservations   = []

            for reservation in reservations:
                reservation_dict = {
                    'thumbnailImage'           : reservation.accommodation.image_set.first().image_url,
                    'startDate'                : reservation.start_date,
                    'endDate'                  : reservation.end_date,
                    'accommodationName'        : reservation.accommodation.title,
                    'accommodationAddress'     : reservation.accommodation.address
                }
                if reservation.status_id == 3:
                    canceled_reservations.append(reservation_dict)
                elif (date.today()-reservation.start_date).days<0:
                    upcoming_reservations.append(reservation_dict)
                else:
                    past_reservations.append(reservation_dict)

            results = {
                'upcomingReservations' : upcoming_reservations,
                'pastReservations'     : past_reservations,
                'canceledReservations' : canceled_reservations
            }
            
            return JsonResponse({'message':'SUCESS','results':results}, status=200)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
