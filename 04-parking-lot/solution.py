from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
import math
import uuid
from decimal import Decimal

# Enum Vehicle Size
class VehicleSize(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3

# Abstract Vehicle
class Vehicle(ABC):
    def get_license_plate(self) -> str:
        return self.license_plate
    
    @abstractmethod
    def get_size(self) -> VehicleSize:
        ...

# Concrete Vehicle
class Motorcycle(Vehicle):
    def __init__(self, license_plate) -> None:
        self.license_plate = license_plate
    
    def get_size(self) -> VehicleSize:
        return VehicleSize.SMALL
    
class Car(Vehicle):
    def __init__(self, license_plate) -> None:
        self.license_plate = license_plate

    def get_size(self) -> VehicleSize:
        return VehicleSize.MEDIUM

class Truck(Vehicle):
    def __init__(self, license_plate) -> None:
        self.license_plate = license_plate
    
    def get_size(self) -> VehicleSize:
        return VehicleSize.LARGE

# Abstract Parking Plot
class ParkingSpot(ABC):
    def __init__(self, spot_number: int) -> None:
        self.spot_number = spot_number
        self.vehicle: Vehicle | None = None
        
    def is_available(self) -> bool:
        return self.vehicle is None
    
    def occupy(self, vehicle: Vehicle) -> None:
        if not self.is_available():
            raise ValueError("Spot is already occupied!")
        self.vehicle = vehicle
    
    def vacate(self) -> None:
        self.vehicle = None
    
    def get_spot_number(self) -> int:
        return self.spot_number
    
    @abstractmethod
    def get_size(self) -> VehicleSize:
        ...

# Concrete Parking Plot
class CompactSpot(ParkingSpot):
    def get_size(self) -> VehicleSize:
        return VehicleSize.SMALL

class RegularSpot(ParkingSpot):
    def get_size(self) -> VehicleSize:
        return VehicleSize.MEDIUM

class OversizedSpot(ParkingSpot):
    def get_size(self) -> VehicleSize:
        return VehicleSize.LARGE

class ParkingManager:
    def __init__(self, available_spots: dict[VehicleSize, list[ParkingSpot]], vehicle_to_spot_map: dict[Vehicle, ParkingSpot]) -> None:
        self.available_spots = available_spots
        self.vehicle_to_spot_map = vehicle_to_spot_map
    def find_spot_for_vehicle(self, vehicle: Vehicle) -> ParkingSpot | None:
        vehicle_size = vehicle.get_size()

        for size in VehicleSize:
            if size.value >= vehicle_size.value:
                spots = self.available_spots[size]
                for spot in spots:
                    if spot.is_available():
                        return spot
        
        return None

    def park_vehicle(self, vehicle: Vehicle) -> ParkingSpot | None:
        spot = self.find_spot_for_vehicle(vehicle)

        if spot is None:
            return None
        
        spot.occupy(vehicle)
        self.vehicle_to_spot_map[vehicle] = spot
        self.available_spots[spot.get_size()].remove(spot)

        return spot
            

    def unpark_vehicle(self, vehicle: Vehicle) -> None:
        spot = self.vehicle_to_spot_map.pop(vehicle, None)
        if spot is not None:
            spot.vacate()
            self.available_spots[spot.get_size()].append(spot)

class Ticket:
    def __init__(self, ticket_id: str, vehicle: Vehicle, parking_spot: ParkingSpot, entry_time: datetime) -> None:
        self.ticket_id = ticket_id
        self.vehicle = vehicle
        self.parking_spot = parking_spot
        self.entry_time = entry_time
        self.exit_time: datetime | None = None 
    
    def calculate_parking_duration(self) -> int:
        end_time = self.exit_time or datetime.now()
        duration = end_time - self.entry_time
        return math.ceil(duration.total_seconds() / 60)
    
    def get_vehicle(self) -> Vehicle:
        return self.vehicle
    
    def get_entry_time(self) -> datetime:
        return self.entry_time
    
    def get_exit_time(self) -> datetime:
        return self.exit_time
    
    def set_exit_time(self, time: datetime):
        self.exit_time = time

# Strategy Pattern
class FareStrategy(ABC):
    @abstractmethod
    def calculate_fare(self, ticket: Ticket, input_fare: Decimal) -> Decimal:
        ...

class BaseFareStrategy(FareStrategy):
    def __init__(self) -> None:
        self.SMALL_VEHICLE_RATE = Decimal("1.0")
        self.MEDIUM_VEHICLE_RATE = Decimal("2.0")
        self.LARGE_VEHICLE_RATE = Decimal("3.0")
    
    def calculate_fare(self, ticket: Ticket, input_fare: Decimal) -> Decimal:
        fare = input_fare
        rate = Decimal("0")
        match ticket.get_vehicle().get_size():
            case VehicleSize.SMALL:
                rate = self.SMALL_VEHICLE_RATE
            case VehicleSize.MEDIUM:
                rate = self.MEDIUM_VEHICLE_RATE
            case VehicleSize.LARGE:
                rate = self.LARGE_VEHICLE_RATE
        
        print("Parking Duration: ", ticket.calculate_parking_duration())
        duration = ticket.calculate_parking_duration()
        return fare + duration * rate

class PeakHoursFareStrategy(FareStrategy):
    def __init__(self) -> None:
        self.PEAK_HOURS_MULTIPLIER = Decimal("1.5")
    
    def is_peak_hours(self, time: datetime) -> bool:
        hour = time.hour
        return (7 <= hour <= 10) or (16 <= hour <= 19)
    
    def calculate_fare(self, ticket: Ticket, input_fare: Decimal) -> Decimal:
        fare = input_fare
        if self.is_peak_hours(ticket.get_entry_time()):
            return fare * self.PEAK_HOURS_MULTIPLIER
        return fare

class FareCalculator:
    def __init__(self, fare_strategies: list[FareStrategy]) -> None:
        self.fare_strategies = fare_strategies
    
    def calculate_fare(self, ticket: Ticket) -> Decimal:
        fare = Decimal("0")
        for fare_strategy in self.fare_strategies:
            fare = fare_strategy.calculate_fare(ticket, fare)
        
        return fare

class ParkingLot:
    def __init__(self, parking_manager: ParkingManager, fare_calculator: FareCalculator) -> None:
        self.parking_manager = parking_manager
        self.fare_calculator = fare_calculator
    def generate_ticket_id(self) -> str:
        id = str(uuid.uuid4())
        return id
    def enter_vehicle(self, vehicle: Vehicle) -> Ticket:
        spot = self.parking_manager.park_vehicle(vehicle)
        if spot is not None:
            ticket = Ticket(
                self.generate_ticket_id(),
                vehicle,
                spot,
                datetime.now()
            )
            return ticket
        
        return None
    
    def leave_vehicle(self, ticket: Ticket) -> Decimal | None:
        if ticket is not None and ticket.get_exit_time() is None:
            ticket.set_exit_time(datetime.now())
            self.parking_manager.unpark_vehicle(ticket.get_vehicle())
            return self.fare_calculator.calculate_fare(ticket)
        return None

if __name__ == "__main__":

    # Create vehicles
    car = Car("CAR-123")
    motorcycle = Motorcycle("BIKE-456")
    truck = Truck("TRUCK-789")

    # Create parking spots
    available_spots = {
        VehicleSize.SMALL: [
            CompactSpot(1)
        ],
        VehicleSize.MEDIUM: [
            RegularSpot(2)
        ],
        VehicleSize.LARGE: [
            OversizedSpot(3)
        ]
    }

    # Create ParkingManager
    parking_manager = ParkingManager(
        available_spots,
        {}
    )

    # Create fare calculator
    fare_calculator = FareCalculator([
        BaseFareStrategy(),
        PeakHoursFareStrategy()
    ])

    # Create ParkingLot
    parking_lot = ParkingLot(
        parking_manager,
        fare_calculator
    )

    # Vehicle enters
    ticket = parking_lot.enter_vehicle(car)

    if ticket is not None:
        print("Vehicle parked!")
        print("Spot:", ticket.parking_spot.get_spot_number())

        import time
        time.sleep(5)
        # Vehicle leaves
        fare = parking_lot.leave_vehicle(ticket)

        print("Fare:", fare)