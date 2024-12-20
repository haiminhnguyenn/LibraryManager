import React, { useEffect, useState } from 'react';
import SearchBar from '../../../search/search_bar';
import Pagination from '../../../pagination/pagination';
import AddBorrowModal from '../../../add_borrow_modal/add_borrow_modal';
import { getAllBorrow, getAllBorrowsByUser, searchBorrow } from '../../../../../../services/admin_services/main_services';
import BorrowHistoryModal from '../../../borrow_history_modal/borrow_history_modal';
import ReturnBookModal from '../../../return_book_modal/return_book_modal';
import { handleRefreshToken } from '../../../../../auth/login_register';
import { ToastContainer } from 'react-toastify';


const ManageBorrowReturn = () => {
    const [currentPage, setCurrentPage] = useState(1);
    const borrowsPerPage = 10;
    const [isAddingBorrow, setIsAddingBorrow] = useState(false);
    const [borrows, setBorrows] = useState([]);
    const [filteredBorrows, setFilteredBorrows] = useState([]);
    const [loading,setLoading] = useState(false)
    const [refreshKey, setRefreshKey] = useState(0);

    const fetchBorrows = async () => {
        try {
            await handleRefreshToken();
            const accessToken = localStorage.getItem('access_token');
            const data = await getAllBorrow(accessToken);
            setBorrows(data || []);
            setFilteredBorrows(data || [])
        } catch (e) {
            console.log(`Error: $e`);
        }
    }

    useEffect(() => {
        fetchBorrows();
    }, [refreshKey])
    //lọc tài khoản

    const totalPages = Math.ceil(filteredBorrows.length / borrowsPerPage);

    const handleSearch = async (searchTerm) => {
        if (!searchTerm.trim()) {
            await fetchBorrows();
        }
        setLoading(true);
        try {
            await handleRefreshToken();
            const accessToken = localStorage.getItem("access_token"); // Lấy JWT Token từ localStorage
            const results = await searchBorrow(searchTerm, accessToken); // Gọi API tìm kiếm
            setFilteredBorrows(results); // Cập nhật kết quả tìm kiếm
        } catch (error) {
            console.error("Lỗi khi tìm kiếm:", error);
        } finally {
            setLoading(false);
        }
    };

    const getCurrentBorrows = () => {
        const startIndex = (currentPage - 1) * borrowsPerPage;
        const endIndex = startIndex + borrowsPerPage;
        return filteredBorrows.slice(startIndex, endIndex);
    };
    const [selectedUserBorrowHistory, setSelectedUserBorrowHistory] = useState([]);
    const [isShowBorrowHistory, setIsShowBorrowHistory] = useState(false);

    const handleShowBorrowHistory = async (userId) => {
        try {
            await handleRefreshToken();
            const accessToken = localStorage.getItem('access_token');
            const data = await getAllBorrowsByUser(accessToken, userId)
            if (data) {
                setSelectedUserBorrowHistory(data)
                setIsShowBorrowHistory(true);
            }
        } catch (error) {
            console.log('error')
        }
    };

    const handleAddnewBorrow = () => {
        setIsAddingBorrow(false); // Đóng modal
    };
    const [selectedBorrowForReturn, setSelectedBorrowForReturn] = useState(null);

    const handleOpenReturnModal = (borrow) => {
        setSelectedBorrowForReturn(borrow);
    };

    const handleReturnBook = () => {
        setSelectedBorrowForReturn(null);
    };
    return (
        <div className="manage-borrows-content">
            <ToastContainer/>
            <div className="searchbar-option">
                <SearchBar
                    onSearch={handleSearch}
                    loading={loading}
                />
                <button className="catalog-button" onClick={() => setIsAddingBorrow(true)} >Tạo lượt mượn sách</button>
            </div>
            <div className="table-container">
                <table>
                    <thead>
                        <tr>
                            <th style={{ width: '200px' }}>ID</th>
                            <th style={{ width: '200px' }}>Email</th>
                            <th style={{ width: '200px' }}>Tên sách</th>
                            <th>SỐ LƯỢNG</th>
                            <th>Ngày mượn</th>
                            <th>Hạn trả</th>
                            <th>Ngày trả</th>
                            <th>Trạng thái</th>
                            <th>Hành động</th>
                        </tr>
                    </thead>
                    <tbody>

                        {getCurrentBorrows().map((borrow,index) => (
                            <tr key={borrow.id}>
                                <td>{index+1}</td>
                                <td>{borrow.user_email}</td>
                                <td>{borrow.book_title}</td>
                                <td className='quantity'>{borrow.quantity}</td>
                                <td>{borrow.borrowDate}</td>
                                <td>{borrow.dueDate}</td>
                                <td>{borrow.returnDate === 'None' ? '-' : borrow.returnDate}</td>
                                <td>{borrow.status === 'borrowing' ? 'Đang mượn' : 'Đã trả'}</td>
                                <td>
                                    <div className="button-option">
                                        <button onClick={() => handleOpenReturnModal(borrow)}
                                        >
                                            Trả sách
                                        </button>
                                        <button onClick={() => handleShowBorrowHistory(borrow.userId)}
                                        >
                                            Xem lịch sử mượn sách
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {/* Phân trang */}
            <Pagination
                currentPage={currentPage}
                totalPages={totalPages}
                onPageChange={setCurrentPage}
                maxPagesToShow={5}
                labels={{
                    previous: 'Trước',
                    next: 'Sau',
                    pageInfo: 'Trang {current} / {total}'
                }}
            />

            {isAddingBorrow && (
                <AddBorrowModal
                    onClose={() => setIsAddingBorrow(false)}
                    onAdd={handleAddnewBorrow}
                    triggerRefresh={() => setRefreshKey((prev) => prev + 1)}
                />
            )}

            {isShowBorrowHistory && (
                <BorrowHistoryModal
                    selectedUserBorrowHistory={selectedUserBorrowHistory}
                    onClose={() => setIsShowBorrowHistory(false)}
                />
            )}

            {selectedBorrowForReturn && (
                <ReturnBookModal
                    borrow={selectedBorrowForReturn}
                    onClose={() => setSelectedBorrowForReturn(null)}
                    onReturn={handleReturnBook}
                    triggerRefresh={() => setRefreshKey((prev) => prev + 1)}
                />
            )}
        </div>
    );
};

export default ManageBorrowReturn;


