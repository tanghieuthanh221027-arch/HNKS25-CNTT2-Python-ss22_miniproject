import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

def show_menu():
    print("\n===== SMART ENERGY MONITOR =====")
    print("1. Xem danh sách thiết bị giám sát")
    print("2. Cập nhật chỉ số điện tiêu thụ")
    print("3. Kích hoạt trạng thái cảnh báo quá tải")
    print("4. Tính tổng lượng điện & Chi phí năng lượng")
    print("5. Thoát chương trình")

def find_device_by_id(devices_list, device_id):
    for device in devices_list:
        if device["id"] == device_id:
            return device
    return None

def input_non_negative_number(message):
    while True:
        try:
            value = float(input(message))

            if value < 0:
                print("[Lỗi] (ERR-E03): Định dạng không hợp lệ! Chỉ số điện phải là số lớn hơn hoặc bằng 0!")
                logger.error("Người dùng nhập số âm")
                continue
            return value

        except ValueError:
            print("[Lỗi] (ERR-E03): Định dạng không hợp lệ! Chỉ số điện phải là số lớn hơn hoặc bằng 0!")
            logger.error("Người dùng nhập sai định dạng số")

def show_devices(devices_list):
    logger.debug(f"Hiển thị {len(devices_list)} thiết bị")

    if not devices_list:
        print("Hệ thống hiện chưa có thiết bị giám sát nào!")
        return

    print(
        f"\n{'MÃ THIẾT BỊ':<15}"
        f"{'VỊ TRÍ PHÂN XƯỞNG':<30}"
        f"{'CHỈ SỐ CŨ':>15}"
        f"{'CHỈ SỐ MỚI':>15}"
        f"{'TRẠNG THÁI':>15}"
    )

    for device in devices_list:
        print(
            f"{device['id']:<15}"
            f"{device['location']:<30}"
            f"{device['old_index']:>15}"
            f"{device['new_index']:>15}"
            f"{device['status']:>15}"
        )

def update_indices(devices_list):
    logger.debug("Bắt đầu cập nhật chỉ số")

    if not devices_list:
        print("Danh sách thiết bị rỗng!")
        return

    while True:
        device_id = input("Nhập mã thiết bị cần cập nhật chỉ số: ").strip()

        if device_id != "":
            break

    device = find_device_by_id(devices_list, device_id)

    if device is None:
        print("[Lỗi] (ERR-E01): Mã thiết bị này không tồn tại trong danh sách hệ thống!")
        logger.error(f"Không tìm thấy thiết bị {device_id}")
        return

    old_index = input_non_negative_number("Nhập chỉ số cũ: ")

    while True:
        new_index = input_non_negative_number("Nhập chỉ số mới: ")

        if new_index < old_index:
            print("[Lỗi] (ERR-E02): Số liệu lỗi! Chỉ số mới không được nhỏ hơn chỉ số cũ!")
            logger.error("Chỉ số mới nhỏ hơn chỉ số cũ")
            continue
        break

    device["old_index"] = old_index
    device["new_index"] = new_index

    print(f"[Thành công]: Đã check-in số liệu cho thiết bị {device_id}")

    logger.info(f"[Thành công]: Đã check-in số liệu cho thiết bị {device_id}")

def trigger_overload_alert(devices_list):
    logger.debug("Kiểm tra trạng thái overload")

    if not devices_list:
        print("Danh sách thiết bị rỗng!")
        return

    device_id = input("Nhập mã thiết bị cần kích hoạt cảnh báo: ").strip()

    device = find_device_by_id(devices_list, device_id)

    if device is None:
        print("[Lỗi] (ERR-E01): Mã thiết bị này không tồn tại trong danh sách hệ thống!")
        logger.error(f"Không tìm thấy thiết bị {device_id}")
        return

    if device["status"] == "Overload":
        print("[Lỗi] (ERR-E04): Thao tác bị hủy! Thiết bị này đã được kích hoạt trạng thái OVERLOAD từ trước!")
        logger.warning(f"Thiết bị {device_id} đã overload trước đó")
        return

    consumption = device["new_index"] - device["old_index"]

    if consumption > 5000:
        device["status"] = "Overload"

        print(f"[Thành công]: Thiết bị {device_id} đã được chuyển sang trạng thái OVERLOAD")

        logger.warning(f"[Cảnh báo]: Thiết bị {device_id} đã vượt ngưỡng tiêu thụ an toàn, chuyển sang OVERLOAD!")
    else:
        print("Thiết bị chưa vượt ngưỡng 5000 kWh.")

def calculate_energy_financials(devices_list):
    logger.debug(f"Đang tính toán chi phí năng lượng cho {len(devices_list)} thiết bị")

    if not devices_list:
        return (0.0, 0.0, 0.0)

    total_kwh = 0

    for device in devices_list:
        total_kwh += (device["new_index"] - device["old_index"])

    discount_percent = 0.0

    if total_kwh >= 50000:
        discount_percent = 3.0

    total_cost = total_kwh * 3000

    final_cost = total_cost * (1 - discount_percent / 100)

    return (
        total_kwh,
        discount_percent,
        final_cost
    )

def main():
    devices_list = [
        {
            "id": "M01",
            "location": "Mechanical Shop A",
            "old_index": 1200,
            "new_index": 4500,
            "status": "Normal"
        },
        {
            "id": "M02",
            "location": "Assembly Line B",
            "old_index": 2300,
            "new_index": 8500,
            "status": "Overload"
        },
        {
            "id": "M03",
            "location": "Packaging Area",
            "old_index": 5000,
            "new_index": 12000,
            "status": "Normal"
        }
    ]

    while True:
        show_menu()

        try:
            choice = int(input("Nhập lựa chọn: "))

            if choice < 1 or choice > 5:
                raise ValueError

        except ValueError:
            print("[Lỗi] (ERR-E05): Lựa chọn sai! Vui lòng nhập đúng số thứ tự chức năng từ 1 đến 5!")
            logger.error("Lựa chọn menu không hợp lệ")
            continue

        if choice == 1:
            show_devices(devices_list)

        elif choice == 2:
            update_indices(devices_list)

        elif choice == 3:
            trigger_overload_alert(devices_list)

        elif choice == 4:
            total_kwh, discount, final_cost = (
                calculate_energy_financials(devices_list)
            )

            print("\n===== BÁO CÁO NĂNG LƯỢNG =====")
            print(f"Tổng điện tiêu thụ: {total_kwh:,.0f} kWh")
            print(f"Chiết khấu áp dụng: {discount}%")
            print(f"Tổng tiền sau chiết khấu: {final_cost:,.0f} VND")

        elif choice == 5:
            print("Cảm ơn bạn đã sử dụng Smart Energy Monitor!")
            logger.info("Thoát chương trình")
            break

if __name__ == "__main__":
    main()